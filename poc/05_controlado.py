#!/usr/bin/env python3
"""H6: conta a forma controlada contra a instrução otimizada.

Não chama API. Não decide H7. Não altera HIPOTESES-v1.md.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARES_V0 = ROOT / "benchmarks" / "datasets" / "pares_v0.json"
CONTROLADO = ROOT / "benchmarks" / "datasets" / "pares_v1_controlado.json"
FORMATOS = ROOT / "benchmarks" / "datasets" / "formatos_v1.json"
HIPOTESES = ROOT / "HIPOTESES-v1.md"
OUT_JSON = ROOT / "benchmarks" / "results" / "poc_v1_controlado.json"
OUT_MD = ROOT / "benchmarks" / "results" / "poc_v1_controlado.md"

CORTESIA = ("por favor", "obrigado", "obrigada", "tudo bem")
ROTULO_LINHA = re.compile(r"^(regras|termo|definições|texto|contexto):\s*$", re.IGNORECASE)
LIMIAR_REDUCAO = 0.15
TETO_PALAVRAS = 20


def carregar_piloto():
    caminho = ROOT / "poc" / "01_tokenizacao.py"
    spec = importlib.util.spec_from_file_location("piloto_v0", caminho)
    if spec is None or spec.loader is None:
        raise RuntimeError("não achei poc/01_tokenizacao.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def segmentos(texto: str) -> list[str]:
    partes: list[str] = []
    for linha in texto.splitlines():
        linha = linha.strip()
        if linha.startswith("- "):
            linha = linha[2:].strip()
        if not linha or ROTULO_LINHA.match(linha):
            continue
        for pedaco in re.split(r"(?<=[.!?])\s+", linha):
            pedaco = pedaco.strip()
            if pedaco:
                partes.append(pedaco)
    return partes


def validar(v0: dict, v1: dict, formatos: dict) -> list[str]:
    erros: list[str] = []
    origem = {item["id"]: item for item in v0["itens"]}
    vistos: set[str] = set()
    if len(v1["itens"]) != len(origem):
        erros.append(f"v1 tem {len(v1['itens'])} itens; v0 tem {len(origem)}")
    for item in v1["itens"]:
        identificador = item["id"]
        if identificador in vistos:
            erros.append(f"{identificador} repetido")
        vistos.add(identificador)
        base = origem.get(identificador)
        if base is None:
            erros.append(f"{identificador} não está no v0")
            continue
        texto = item["pt_controlado"]
        otimizado = base["instrucao"]["pt_otimizado"]
        if texto == otimizado:
            erros.append(f"{identificador} repete pt_otimizado")
        if "ASD-STE100" in texto.upper():
            erros.append(f"{identificador} pede a sigla da especificação")
        baixo = texto.casefold()
        for cortesia in CORTESIA:
            if cortesia in baixo:
                erros.append(f"{identificador} contém {cortesia!r}")
        for marcador in base["marcadores_pt"]:
            if marcador not in texto:
                erros.append(f"{identificador} sem marcador {marcador!r}")
        for pedaco in segmentos(texto):
            palavras = pedaco.split()
            if len(palavras) > TETO_PALAVRAS:
                erros.append(f"{identificador} tem {len(palavras)} palavras em {pedaco!r}")
    faltam = set(origem) - vistos
    for identificador in sorted(faltam):
        erros.append(f"{identificador} sem forma controlada")

    ids_formato = set(formatos["itens"])
    excluidos = set(formatos["excluidos"])
    if ids_formato & excluidos:
        erros.append("um item está nos dois lados do recorte de H7")
    if ids_formato | excluidos != set(origem):
        erros.append("H7 não cobre o recorte do v0")
    for nome in ("frases", "mermaid", "html"):
        if not formatos["sufixo"].get(nome, "").strip():
            erros.append(f"sufixo {nome} vazio")
    if "video" in formatos["sufixo"] or "vídeo" in formatos["sufixo"]:
        erros.append("vídeo entrou como braço")
    return erros


def decidir_h6(reducao: float | None) -> str:
    if reducao is None:
        return "inconclusiva"
    if reducao >= LIMIAR_REDUCAO:
        return "recusa H6 neste conjunto"
    return "compatível com H6 neste conjunto"


def medir(piloto, v0: dict, v1: dict, codificador) -> dict:
    origem = {item["id"]: item for item in v0["itens"]}
    linhas = []
    for item in v1["itens"]:
        base = origem[item["id"]]
        registro = {"id": item["id"]}
        for braco, instrucao in (
            ("pt_otimizado", base["instrucao"]["pt_otimizado"]),
            ("pt_controlado", item["pt_controlado"]),
        ):
            payload = f"{piloto.nfc(base['rotulo_pt'])}\n{piloto.nfc(base['fonte_pt'])}"
            completo = piloto.montar_completo(instrucao, base["rotulo_pt"], base["fonte_pt"])
            registro[braco] = {
                "instrucao": piloto.medidas(instrucao, codificador),
                "payload": piloto.medidas(payload, codificador),
                "completo": piloto.medidas(completo, codificador),
            }
        linhas.append(registro)
    instrucao = piloto.contraste(linhas, "pt_controlado", "pt_otimizado", "instrucao")
    completo = piloto.contraste(linhas, "pt_controlado", "pt_otimizado", "completo")
    return {
        "itens": linhas,
        "contrastes": {"h6_instrucao": instrucao, "h6_completo": completo},
        "decisao_h6": decidir_h6(instrucao["reducao"]),
    }


def markdown(relatorio: dict, piloto) -> str:
    primario = relatorio["medicoes"]["o200k_base"]
    instrucao = primario["contrastes"]["h6_instrucao"]
    completo = primario["contrastes"]["h6_completo"]
    linhas = [
        "# Forma controlada, v1",
        "",
        "Gerado por `poc/05_controlado.py`. Não edite os números à mão.",
        "",
        f"Dataset controlado: `{relatorio['controlado_sha256']}`",
        f"Hipóteses v1: `{relatorio['hipoteses_sha256']}`",
        "",
        "H6 compara a soma da instrução `pt_controlado` com a soma da instrução `pt_otimizado`. Redução de 15% ou mais recusa H6 neste conjunto. O prompt completo não decide.",
        "",
        f"Decisão no `o200k_base`: {primario['decisao_h6']}.",
        "",
        "| Escopo | Tokens otimizado | Tokens controlado | Razão | Redução |",
        "| --- | ---: | ---: | ---: | ---: |",
        (
            f"| Instrução | {instrucao['tokens_direita']} | {instrucao['tokens_esquerda']} | "
            f"{piloto.fmt(instrucao['razao_tokens'])} | {piloto.fmt_pct(instrucao['reducao'])} |"
        ),
        (
            f"| Completo | {completo['tokens_direita']} | {completo['tokens_esquerda']} | "
            f"{piloto.fmt(completo['razao_tokens'])} | {piloto.fmt_pct(completo['reducao'])} |"
        ),
        "",
        "Razão acima de 1: a forma controlada gastou mais tokens do que a otimizada. Redução negativa é aumento.",
        "",
        "## Por item, instrução, o200k_base",
        "",
        "| Item | Otimizado | Controlado |",
        "| --- | ---: | ---: |",
    ]
    for item in primario["itens"]:
        linhas.append(
            f"| {item['id']} | {item['pt_otimizado']['instrucao']['tokens']} | "
            f"{item['pt_controlado']['instrucao']['tokens']} |"
        )
    secundario = relatorio["medicoes"]["cl100k_base"]["contrastes"]["h6_instrucao"]
    linhas.extend(
        [
            "",
            (
                f"No `cl100k_base`, a instrução controlada soma {secundario['tokens_esquerda']} tokens "
                f"e a otimizada soma {secundario['tokens_direita']} "
                f"(razão {piloto.fmt(secundario['razao_tokens'])}). Esse encoding não decide H6."
            ),
            "",
            "## H7",
            "",
            "Os estímulos estão em `benchmarks/datasets/formatos_v1.json`. A saída não foi medida. Sem o `usage` da API, esta seção não recebe número.",
            "",
        ]
    )
    return "\n".join(linhas)


def main() -> int:
    piloto = carregar_piloto()
    v0 = json.loads(PARES_V0.read_text(encoding="utf-8"))
    v1 = json.loads(CONTROLADO.read_text(encoding="utf-8"))
    formatos = json.loads(FORMATOS.read_text(encoding="utf-8"))
    erros = validar(v0, v1, formatos)
    if erros:
        for erro in erros:
            print(erro, file=sys.stderr)
        return 1
    if "--checar" in sys.argv:
        print(f"forma controlada ok ({len(v1['itens'])} itens); H7 sem contagem")
        return 0

    codificadores = piloto.carregar_codificadores()
    medicoes = {
        nome: medir(piloto, v0, v1, codificador)
        for nome, codificador in codificadores.items()
    }
    relatorio = {
        "versao": "v1",
        "n_itens": len(v1["itens"]),
        "dataset_v0_sha256": piloto.sha256_arquivo(PARES_V0),
        "controlado_sha256": piloto.sha256_arquivo(CONTROLADO),
        "formatos_sha256": piloto.sha256_arquivo(FORMATOS),
        "hipoteses_sha256": piloto.sha256_arquivo(HIPOTESES),
        "encoding_primario": "o200k_base",
        "aviso": "H6 é descritiva neste conjunto. H7 não foi medida.",
        "medicoes": medicoes,
    }
    OUT_JSON.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown(relatorio, piloto), encoding="utf-8")
    decisao = medicoes["o200k_base"]
    reducao = decisao["contrastes"]["h6_instrucao"]["reducao"]
    print(f"H6 reducao instrucao: {reducao:.3f} — {decisao['decisao_h6']}")
    print(f"escreveu {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
