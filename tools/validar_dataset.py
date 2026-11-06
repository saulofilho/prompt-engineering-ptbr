#!/usr/bin/env python3
"""Valida a forma do dataset de pares antes da discussão dos números.

Checa o que o CONTRIBUTING.md exige, com erro legível em vez de KeyError:
campos obrigatórios por item, braços de instrução presentes, marcadores
compartilhados entre pt_coloquial e pt_otimizado, e pt_vago sem conter
todos os marcadores. Python puro, sem dependência externa.

    python3 tools/validar_dataset.py                      # valida pares_v0 e v1
    python3 tools/validar_dataset.py caminho/para.json    # valida um arquivo
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASETS = ROOT / "benchmarks" / "datasets"
PADRAO = [
    DATASETS / "pares_v0.json",
    DATASETS / "pares_v1_controlado.json",
]

CAMPOS_ITEM = {
    "id",
    "tarefa",
    "rotulo_en",
    "rotulo_pt",
    "marcadores_en",
    "marcadores_pt",
    "fonte_en",
    "fonte_pt",
    "instrucao",
}
BRACOS = {"en", "pt_paralelo", "pt_coloquial", "pt_vago", "pt_otimizado"}


def validar_controlado(caminho: Path, itens: list) -> list[str]:
    """Schema da forma controlada v1: cada item é {id, pt_controlado}."""
    erros: list[str] = []
    ids_vistos: set[str] = set()
    for pos, item in enumerate(itens):
        rotulo = item.get("id", f"#{pos}") if isinstance(item, dict) else f"#{pos}"
        if not isinstance(item, dict) or "id" not in item or "pt_controlado" not in item:
            erros.append(f"{caminho.name}: item {rotulo} sem 'id' ou 'pt_controlado'")
            continue
        if not isinstance(item["pt_controlado"], str) or not item["pt_controlado"].strip():
            erros.append(f"{caminho.name}: item {rotulo} com 'pt_controlado' vazio")
        if item["id"] in ids_vistos:
            erros.append(f"{caminho.name}: id duplicado {item['id']!r}")
        ids_vistos.add(item["id"])
    return erros


def validar_conjunto(caminho: Path) -> list[str]:
    erros: list[str] = []
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{caminho.name}: não foi possível ler/parsear: {exc}"]

    if not isinstance(dados, dict) or "itens" not in dados:
        return [f"{caminho.name}: falta a chave de topo 'itens'"]

    itens = dados["itens"]
    if not isinstance(itens, list) or not itens:
        return [f"{caminho.name}: 'itens' deve ser lista não vazia"]

    # A forma controlada v1 tem schema próprio (id + pt_controlado).
    primeiro = itens[0]
    if isinstance(primeiro, dict) and "pt_controlado" in primeiro and "instrucao" not in primeiro:
        return validar_controlado(caminho, itens)

    ids_vistos: set[str] = set()
    for pos, item in enumerate(itens):
        rotulo = item.get("id", f"#{pos}")
        if not isinstance(item, dict):
            erros.append(f"{caminho.name}: item {rotulo} não é objeto")
            continue

        faltam = CAMPOS_ITEM - set(item)
        if faltam:
            erros.append(f"{caminho.name}: item {rotulo} sem campos {sorted(faltam)}")

        if "id" in item:
            if item["id"] in ids_vistos:
                erros.append(f"{caminho.name}: id duplicado {item['id']!r}")
            ids_vistos.add(item["id"])

        instrucao = item.get("instrucao")
        if not isinstance(instrucao, dict):
            erros.append(f"{caminho.name}: item {rotulo} com 'instrucao' ausente ou inválida")
            continue
        faltam_bracos = BRACOS - set(instrucao)
        if faltam_bracos:
            erros.append(f"{caminho.name}: item {rotulo} sem braços {sorted(faltam_bracos)}")
            continue

        marcadores = item.get("marcadores_pt")
        if not isinstance(marcadores, list) or not marcadores:
            erros.append(f"{caminho.name}: item {rotulo} sem lista 'marcadores_pt'")
            continue

        for braco in ("pt_paralelo", "pt_coloquial", "pt_otimizado"):
            texto = instrucao.get(braco, "")
            ausentes = [m for m in marcadores if m not in texto]
            if ausentes:
                erros.append(
                    f"{caminho.name}: item {rotulo} braço {braco} sem marcador(es) {ausentes}"
                )

        vago = instrucao.get("pt_vago", "")
        if all(m in vago for m in marcadores):
            erros.append(
                f"{caminho.name}: item {rotulo} braço pt_vago contém todos os marcadores "
                "(deveria omitir ao menos um)"
            )

    return erros


def main(argv: list[str]) -> int:
    alvos = [Path(a) for a in argv] or PADRAO
    todos: list[str] = []
    for caminho in alvos:
        todos.extend(validar_conjunto(caminho))

    if todos:
        print("dataset inválido:", file=sys.stderr)
        for erro in todos:
            print(f"  - {erro}", file=sys.stderr)
        return 1
    print(f"dataset válido ({len(alvos)} arquivo(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
