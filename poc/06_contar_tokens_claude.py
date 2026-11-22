#!/usr/bin/env python3
"""Conta a razão PT/EN do Claude pelo count_tokens, sem gerar resposta.

O endpoint não cobra por contagem, mas recusa conta sem saldo de créditos
(HTTP 400, visto em 2026-11-22). O número é estimativa do provedor. Este script
nunca chama /v1/messages, que é pago. A chave pode ser digitada no prompt
oculto: exportá-la habilitaria também as chamadas pagas de poc/04.
"""

from __future__ import annotations

import getpass
import importlib.util
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRACOS = ("en", "pt_paralelo")


def carregar(caminho: Path, nome: str):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"não foi possível carregar {caminho}")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def obter_chave() -> str:
    segredo = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not segredo:
        if not sys.stdin.isatty():
            raise RuntimeError("sem chave: rode num terminal para digitá-la no prompt oculto")
        segredo = getpass.getpass("Chave da API Anthropic (não aparece, não é salva): ").strip()
    if not segredo:
        raise RuntimeError("chave vazia")
    # O http.client repete o valor do cabeçalho inválido na exceção, o que vazaria a chave.
    if not all("!" <= caractere <= "~" for caractere in segredo):
        raise RuntimeError("chave com espaço ou caractere inválido")
    return segredo


def contar(gerar, poc, provedor: dict, itens: list[dict], segredo: str) -> list[dict]:
    url = provedor["url"] + "/count_tokens"
    cabecalhos = {
        "x-api-key": segredo,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    linhas = []
    for item in itens:
        linha = {"id": item["id"]}
        for braco in BRACOS:
            mensagens = [{"role": "user", "content": gerar.prompt_de(poc, item, braco)}]
            dados = gerar.post(url, {"model": provedor["model"], "messages": mensagens}, cabecalhos)
            tokens = dados.get("input_tokens")
            if type(tokens) is not int or tokens <= 0:
                raise RuntimeError(f"resposta sem input_tokens válido em {item['id']} {braco}")
            linha[braco] = tokens
        linhas.append(linha)
        print(f"  {item['id']}: en={linha['en']} pt={linha['pt_paralelo']}", flush=True)
    return linhas


def main() -> int:
    poc = carregar(ROOT / "poc" / "01_tokenizacao.py", "poc_tokenizacao")
    gerar = carregar(ROOT / "poc" / "04_gerar_e_avaliar.py", "gerar_e_avaliar")
    provedor = next(item for item in gerar.PROVEDORES if item["id"] == "claude")
    try:
        conjunto = json.loads(gerar.DATASET.read_text(encoding="utf-8"))
        erros = poc.validar_marcadores(conjunto)
        if erros:
            raise RuntimeError("; ".join(erros))
        relatorio = json.loads(gerar.OUT_JSON.read_text(encoding="utf-8"))
        segredo = obter_chave()
        print(f"contando em {provedor['model']} (count_tokens, sem geração)...", flush=True)
        linhas = contar(gerar, poc, provedor, conjunto["itens"], segredo)
    except (RuntimeError, OSError, ValueError) as exc:
        print(f"nada foi gravado: {exc}", file=sys.stderr)
        return 1
    except (KeyboardInterrupt, EOFError):
        print("cancelado; nada foi gravado", file=sys.stderr)
        return 1

    en = sum(linha["en"] for linha in linhas)
    pt = sum(linha["pt_paralelo"] for linha in linhas)
    contagem = {
        "id": provedor["id"],
        "model": provedor["model"],
        "origem": "count_tokens",
        "aviso": "Estimativa do provedor. Inclui envelope da mensagem. Não mede saída nem qualidade.",
        "contado_em": datetime.now(timezone.utc).date().isoformat(),
        "dataset_sha256": poc.sha256_arquivo(gerar.DATASET),
        "tokens_en": en,
        "tokens_pt": pt,
        "razao_pt_en": pt / en,
        "itens": linhas,
    }
    gerar.OUT_CONTAGEM.write_text(
        json.dumps(contagem, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    gerar.OUT_API.write_text(
        gerar.markdown_api(relatorio, gerar.ler_contagem()), encoding="utf-8"
    )
    print(f"PT/EN {provedor['model']}: {pt}/{en} = {pt / en:.3f}".replace(".", ","))
    print(f"escreveu {gerar.OUT_API}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
