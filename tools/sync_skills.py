#!/usr/bin/env python3
"""Espelha `skills/` em `.cursor/skills/`.

`skills/` é a fonte única. O Cursor no Windows não segue o link simbólico
do Linux, então mantemos uma cópia versionada em `.cursor/skills/`. Copiar
à mão garante divergência silenciosa; este script sincroniza e, com
`--check`, falha quando as duas árvores divergem (uso em CI).

    python3 tools/sync_skills.py          # copia skills/ -> .cursor/skills/
    python3 tools/sync_skills.py --check  # só verifica; sai 1 se divergir
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGEM = ROOT / "skills"
DESTINO = ROOT / ".cursor" / "skills"


def arquivos(base: Path) -> set[Path]:
    return {caminho.relative_to(base) for caminho in base.rglob("*") if caminho.is_file()}


def divergencias() -> list[str]:
    erros: list[str] = []
    na_origem = arquivos(ORIGEM)
    no_destino = arquivos(DESTINO) if DESTINO.exists() else set()

    for relativo in sorted(na_origem - no_destino):
        erros.append(f"falta em .cursor/skills: {relativo}")
    for relativo in sorted(no_destino - na_origem):
        erros.append(f"sobra em .cursor/skills (não existe em skills/): {relativo}")
    for relativo in sorted(na_origem & no_destino):
        if not filecmp.cmp(ORIGEM / relativo, DESTINO / relativo, shallow=False):
            erros.append(f"conteúdo divergente: {relativo}")
    return erros


def sincronizar() -> None:
    if DESTINO.exists():
        shutil.rmtree(DESTINO)
    shutil.copytree(ORIGEM, DESTINO)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="não copia; sai com código 1 se .cursor/skills divergir de skills/",
    )
    args = parser.parse_args()

    if not ORIGEM.exists():
        print(f"erro: {ORIGEM} não existe", file=sys.stderr)
        return 2

    erros = divergencias()
    if args.check:
        if erros:
            print(".cursor/skills divergiu de skills/:", file=sys.stderr)
            for erro in erros:
                print(f"  - {erro}", file=sys.stderr)
            print("\nrode: python3 tools/sync_skills.py", file=sys.stderr)
            return 1
        print(".cursor/skills em dia com skills/")
        return 0

    if not erros:
        print(".cursor/skills já estava em dia; nada a copiar")
        return 0
    sincronizar()
    print(f"sincronizado skills/ -> .cursor/skills/ ({len(erros)} ajuste(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
