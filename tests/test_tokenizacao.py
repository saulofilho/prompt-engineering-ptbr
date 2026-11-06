"""Testes das funções puras do piloto de tokenização.

A contagem em si precisa de tiktoken; onde ele falta, o teste é pulado.
As funções de normalização e a validação de marcadores não dependem dele,
mas o módulo importa tiktoken no topo, então pulamos a importação inteira
quando a lib não está instalada.
"""

from __future__ import annotations

import json

import pytest
from conftest import ROOT, carregar

pytest.importorskip("tiktoken")
poc = carregar(ROOT / "poc" / "01_tokenizacao.py", "poc_tokenizacao")


def test_nfc_idempotente():
    assert poc.nfc("ação") == poc.nfc(poc.nfc("ação"))


def test_sem_diacriticos_remove_acentos():
    assert poc.sem_diacriticos("prazo é vencível") == "prazo e vencivel"


def test_validar_marcadores_sem_erro_no_dataset():
    conjunto = json.loads(
        (ROOT / "benchmarks" / "datasets" / "pares_v0.json").read_text(encoding="utf-8")
    )
    assert poc.validar_marcadores(conjunto) == []


def test_marcador_ausente_e_reportado():
    conjunto = {
        "itens": [
            {
                "id": "t",
                "marcadores_pt": ["ALVO"],
                "marcadores_en": [],
                "instrucao": {
                    "pt_paralelo": "sem o termo",
                    "pt_coloquial": "ALVO",
                    "pt_otimizado": "ALVO",
                    "pt_vago": "sem o termo",
                },
            }
        ]
    }
    erros = poc.validar_marcadores(conjunto)
    assert any("ALVO" in e for e in erros)
