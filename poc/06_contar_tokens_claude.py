#!/usr/bin/env python3
"""Conta a razão PT/EN do Claude pelo count_tokens, sem gerar resposta.

O endpoint não cobra por contagem, mas recusa conta sem saldo de créditos
(HTTP 400, visto em 2026-11-22). O número é estimativa do provedor. Este script
nunca chama /v1/messages, que é pago. A chave pode ser digitada no prompt
oculto: exportá-la habilitaria também as chamadas pagas de poc/04.

A mecânica serve também a poc/07, que conta no Gemini.
"""

from __future__ import annotations

import getpass
import importlib.util
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRACOS = ("en", "pt_paralelo")
CONTADORES = {
    "claude": {
        "nome": "Anthropic",
        "env": "ANTHROPIC_API_KEY",
        "origem": "count_tokens",
        "campo": "input_tokens",
        "pausa": 0,
        "aviso": "Estimativa do provedor. Inclui envelope da mensagem. Não mede saída nem qualidade.",
    },
    "gemini": {
        "nome": "do Gemini",
        # Sem variável de ambiente: GOOGLE_API_KEY costuma ser de projeto com faturamento.
        "env": None,
        "origem": "countTokens",
        "campo": "totalTokens",
        # O limite por minuto do nível gratuito não é publicado.
        "pausa": 2,
        "aviso": "Contagem do provedor, sem declaração de exatidão. Não mede saída nem qualidade.",
    },
}


def carregar(caminho: Path, nome: str):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"não foi possível carregar {caminho}")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def obter_chave(gerar, contador: dict) -> str:
    segredo = os.environ.get(contador["env"], "").strip() if contador["env"] else ""
    if not segredo:
        if not sys.stdin.isatty():
            raise RuntimeError("sem chave: rode num terminal para digitá-la no prompt oculto")
        segredo = getpass.getpass(f"Chave da API {contador['nome']} (não aparece, não é salva): ").strip()
    if not segredo:
        raise RuntimeError("chave vazia")
    gerar.validar_segredo(segredo)
    return segredo


def requisicao(provedor: dict, texto: str, segredo: str) -> tuple[str, dict, dict]:
    """Só endpoints de contagem. Nenhum ramo aqui gera resposta."""
    if provedor["tipo"] == "anthropic":
        return (
            provedor["url"] + "/count_tokens",
            {"model": provedor["model"], "messages": [{"role": "user", "content": texto}]},
            {
                "x-api-key": segredo,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
        )
    if provedor["tipo"] == "gemini":
        return (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{provedor['model']}:countTokens",
            {"contents": [{"role": "user", "parts": [{"text": texto}]}]},
            {"x-goog-api-key": segredo, "content-type": "application/json"},
        )
    raise RuntimeError(f"sem contagem para {provedor['tipo']}")


def contar(gerar, poc, provedor: dict, itens: list[dict], segredo: str) -> list[dict]:
    contador = CONTADORES[provedor["id"]]
    linhas = []
    for item in itens:
        linha = {"id": item["id"]}
        for braco in BRACOS:
            dados = gerar.post(*requisicao(provedor, gerar.prompt_de(poc, item, braco), segredo))
            tokens = dados.get(contador["campo"])
            if type(tokens) is not int or tokens <= 0:
                raise RuntimeError(f"resposta sem {contador['campo']} válido em {item['id']} {braco}")
            linha[braco] = tokens
            time.sleep(contador["pausa"])
        linhas.append(linha)
        print(f"  {item['id']}: en={linha['en']} pt={linha['pt_paralelo']}", flush=True)
    return linhas


def main(id_provedor: str = "claude") -> int:
    poc = carregar(ROOT / "poc" / "01_tokenizacao.py", "poc_tokenizacao")
    gerar = carregar(ROOT / "poc" / "04_gerar_e_avaliar.py", "gerar_e_avaliar")
    provedor = next(item for item in gerar.PROVEDORES if item["id"] == id_provedor)
    contador = CONTADORES[id_provedor]
    segredo = None
    try:
        conjunto = json.loads(gerar.DATASET.read_text(encoding="utf-8"))
        erros = poc.validar_marcadores(conjunto)
        if erros:
            raise RuntimeError("; ".join(erros))
        relatorio = json.loads(gerar.OUT_JSON.read_text(encoding="utf-8"))
        segredo = obter_chave(gerar, contador)
        print(f"contando em {provedor['model']} ({contador['origem']}, sem geração)...", flush=True)
        linhas = contar(gerar, poc, provedor, conjunto["itens"], segredo)
    except (RuntimeError, OSError, ValueError) as exc:
        print(f"nada foi gravado: {gerar.ocultar(str(exc), segredo)}", file=sys.stderr)
        return 1
    except (KeyboardInterrupt, EOFError):
        print("cancelado; nada foi gravado", file=sys.stderr)
        return 1

    en = sum(linha["en"] for linha in linhas)
    pt = sum(linha["pt_paralelo"] for linha in linhas)
    contagem = {
        "id": provedor["id"],
        "model": provedor["model"],
        "origem": contador["origem"],
        "aviso": contador["aviso"],
        "contado_em": datetime.now(timezone.utc).date().isoformat(),
        "dataset_sha256": poc.sha256_arquivo(gerar.DATASET),
        "tokens_en": en,
        "tokens_pt": pt,
        "razao_pt_en": pt / en,
        "itens": linhas,
    }
    gerar.caminho_contagem(id_provedor).write_text(
        json.dumps(contagem, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    gerar.OUT_API.write_text(
        gerar.markdown_api(relatorio, gerar.ler_contagens()), encoding="utf-8"
    )
    razao = f"{pt / en:.3f}".replace(".", ",")
    print(f"PT/EN {provedor['model']}: {pt}/{en} = {razao}")
    print(f"escreveu {gerar.OUT_API}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
