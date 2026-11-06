"""Testes do validador de schema do dataset."""

from __future__ import annotations

import json

from conftest import ROOT, carregar

validar = carregar(ROOT / "tools" / "validar_dataset.py", "validar_dataset")


def test_datasets_do_repo_sao_validos():
    assert validar.main([]) == 0


def test_item_sem_campo_obrigatorio_falha(tmp_path):
    ruim = {"itens": [{"id": "x"}]}
    arq = tmp_path / "ruim.json"
    arq.write_text(json.dumps(ruim), encoding="utf-8")
    erros = validar.validar_conjunto(arq)
    assert erros


def test_pt_vago_com_todos_marcadores_falha(tmp_path):
    item = {
        "id": "y",
        "tarefa": "resumo",
        "rotulo_en": "Text:",
        "rotulo_pt": "Texto:",
        "marcadores_en": ["a"],
        "marcadores_pt": ["ALVO"],
        "fonte_en": "x",
        "fonte_pt": "x",
        "instrucao": {
            "en": "ALVO",
            "pt_paralelo": "ALVO",
            "pt_coloquial": "ALVO",
            "pt_otimizado": "ALVO",
            "pt_vago": "ALVO aqui também",
        },
    }
    arq = tmp_path / "vago.json"
    arq.write_text(json.dumps({"itens": [item]}), encoding="utf-8")
    erros = validar.validar_conjunto(arq)
    assert any("pt_vago" in e for e in erros)


def test_forma_controlada_schema_proprio(tmp_path):
    bom = {"itens": [{"id": "z", "pt_controlado": "Resuma em cinco tópicos."}]}
    arq = tmp_path / "ctrl.json"
    arq.write_text(json.dumps(bom), encoding="utf-8")
    assert validar.validar_conjunto(arq) == []

    ruim = {"itens": [{"id": "z"}]}
    arq.write_text(json.dumps(ruim), encoding="utf-8")
    assert validar.validar_conjunto(arq)
