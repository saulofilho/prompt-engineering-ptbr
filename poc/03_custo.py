#!/usr/bin/env python3
"""Converte tokens já medidos em dólar, com a tabela datada.

Só entra modelo que tenha preço publicado neste repositório e tokens
medidos no benchmark. Claude, Gemini e Sabiá não recebem o preço de
outro vocabulário, nem um dólar sem contagem.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRECOS = ROOT / "benchmarks" / "datasets" / "precos_v0.json"
BENCHMARK = ROOT / "benchmarks" / "results" / "benchmark_modelos_ptbr_en.json"
OUT_JSON = ROOT / "benchmarks" / "results" / "custo_usd.json"
OUT_MD = ROOT / "benchmarks" / "results" / "custo_usd.md"

PRECO_POR_ID = {
    "gpt-4o": "gpt-4o",
}


def usd(tokens: int, por_milhao: float) -> float:
    return tokens / 1_000_000 * por_milhao


def brl_para_usd(valor_brl: float, cambio: float) -> float:
    return valor_brl / cambio


def fmt(valor: float | None) -> str:
    if valor is None:
        return "—"
    return f"{valor:.6f}".replace(".", ",")


def main() -> int:
    precos = json.loads(PRECOS.read_text(encoding="utf-8"))
    benchmark = json.loads(BENCHMARK.read_text(encoding="utf-8"))
    tabela = {item["id"]: item for item in precos["modelos"]}
    cambio = precos["cambio_brl_por_usd"]["valor"]
    linhas = []
    for modelo in benchmark["modelos"]:
        preco_id = PRECO_POR_ID.get(modelo["id"])
        preco = tabela.get(preco_id) if preco_id else None
        if modelo.get("status") != "medido" or preco is None:
            linhas.append(
                {
                    "id": modelo["id"],
                    "rotulo": modelo["rotulo"],
                    "status": "sem_dolar",
                    "motivo": (
                        "sem tokens medidos neste benchmark"
                        if modelo.get("status") != "medido"
                        else "sem preço de tabela verificado para este vocabulário"
                    ),
                }
            )
            continue
        en = modelo["medicao"]["somas"]["en"]["completo"]
        pt = modelo["medicao"]["somas"]["pt_paralelo"]["completo"]
        entrada = preco["entrada_usd_por_milhao"]
        linhas.append(
            {
                "id": modelo["id"],
                "rotulo": f"{preco['rotulo']} (tokens de {modelo['rotulo']})",
                "status": "medido",
                "preco_id": preco_id,
                "fonte": preco["fonte"],
                "tokens_en": en,
                "tokens_pt": pt,
                "usd_entrada_en": usd(en, entrada),
                "usd_entrada_pt": usd(pt, entrada),
                "usd_entrada_diferenca": usd(pt - en, entrada),
                "saida": None,
                "nota": "Só a entrada dos doze prompts. A saída não foi gerada neste arquivo.",
            }
        )

    relatorio = {
        "consultado_em": precos["consultado_em"],
        "cambio_brl_por_usd": cambio,
        "aviso": "Dólar de entrada a partir de tokens medidos. Sem saída e sem preço emprestado.",
        "modelos": linhas,
    }
    OUT_JSON.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = [
        "# Custo em dólar da entrada",
        "",
        "Gerado por `poc/03_custo.py`. Preços em `benchmarks/datasets/precos_v0.json`, consultados em "
        f"{precos['consultado_em']}. A conta é tokens ÷ 1.000.000 × preço de entrada. Não inclui saída, cache, lote nem reprompt.",
        "",
        "Modelo aberto sem preço de hospedeiro, e bot sem tokens medidos, ficam sem dólar. O preço de um não preenche o outro.",
        "",
        "| Modelo | Tokens EN | Tokens PT-BR | USD entrada EN | USD entrada PT-BR | Diferença |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for linha in linhas:
        if linha["status"] != "medido":
            md.append(f"| {linha['rotulo']} | — | — | sem dólar | sem dólar | {linha['motivo']} |")
            continue
        md.append(
            "| {rotulo} | {en} | {pt} | {uen} | {upt} | {dif} |".format(
                rotulo=linha["rotulo"],
                en=linha["tokens_en"],
                pt=linha["tokens_pt"],
                uen=fmt(linha["usd_entrada_en"]),
                upt=fmt(linha["usd_entrada_pt"]),
                dif=fmt(linha["usd_entrada_diferenca"]),
            )
        )
    md.extend(
        [
            "",
            "A diferença é o que os doze prompts em português acrescentam na entrada, no preço de tabela daquele modelo. Não é o custo do fluxo: falta a resposta.",
            "",
            "Sabiá-4, quando houver tokens da API, usa a tabela em real (R$ 5 entrada e R$ 20 saída por milhão) e a taxa aproximada de R$ 5,14 por dólar publicada pela Maritaca. Sem essa contagem, a linha continua vazia.",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"escreveu {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
