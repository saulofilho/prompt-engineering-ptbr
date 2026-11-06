"""Carregadores compartilhados: os scripts vivem em poc/ e tools/, fora de um
pacote importável, então os testes os carregam por caminho."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def carregar(caminho: Path, nome: str):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    assert spec is not None and spec.loader is not None, caminho
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nome] = modulo
    spec.loader.exec_module(modulo)
    return modulo
