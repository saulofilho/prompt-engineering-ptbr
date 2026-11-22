"""Testa poc/06 sem rede: só count_tokens, nada parcial, chave fora da saída."""

from __future__ import annotations

import json

import pytest
from conftest import ROOT, carregar

pytest.importorskip("tiktoken")
contador = carregar(ROOT / "poc" / "06_contar_tokens_claude.py", "contar_tokens_claude")

CHAVE = "segredo-teste"


@pytest.fixture
def cenario(tmp_path, monkeypatch):
    gerar = carregar(ROOT / "poc" / "04_gerar_e_avaliar.py", "gerar_para_contagem")
    poc = carregar(ROOT / "poc" / "01_tokenizacao.py", "poc_para_contagem")
    relatorio = {
        "modelos": [
            {"id": p["id"], "rotulo": p["rotulo"], "status": "nao-medido"} for p in gerar.PROVEDORES
        ]
    }
    for nome in ("OUT_JSON", "OUT_API"):
        monkeypatch.setattr(gerar, nome, tmp_path / getattr(gerar, nome).name)
    gerar.OUT_JSON.write_text(json.dumps(relatorio), encoding="utf-8")
    monkeypatch.setattr(
        contador, "carregar", lambda caminho, nome: poc if nome == "poc_tokenizacao" else gerar
    )
    monkeypatch.setenv("ANTHROPIC_API_KEY", CHAVE)
    chamadas = []

    def post(url, payload, headers):
        chamadas.append((url, payload))
        return {"input_tokens": 12 if len(chamadas) % 2 == 0 else 10}

    monkeypatch.setattr(gerar, "post", post)
    return gerar, relatorio, chamadas


def test_so_chama_count_tokens(cenario):
    gerar, _, chamadas = cenario
    assert contador.main() == 0
    assert len(chamadas) == 24
    for url, payload in chamadas:
        assert url == "https://api.anthropic.com/v1/messages/count_tokens"
        assert set(payload) == {"model", "messages"}


def test_grava_so_a_linha_do_claude(cenario):
    gerar, _, _ = cenario
    assert contador.main() == 0
    tabela = gerar.OUT_API.read_text(encoding="utf-8")
    assert "| Claude Haiku 4.5 | 120 | 144 | 1,200 | count_tokens" in tabela
    assert tabela.count("não medido") == 3


def test_chave_nao_vai_para_arquivo_nem_saida(cenario, capsys):
    gerar, _, _ = cenario
    assert contador.main() == 0
    saida = capsys.readouterr()
    assert CHAVE not in saida.out + saida.err
    assert CHAVE not in gerar.caminho_contagem("claude").read_text(encoding="utf-8")
    assert CHAVE not in gerar.OUT_API.read_text(encoding="utf-8")


@pytest.mark.parametrize("resposta", [{}, {"input_tokens": 0}, {"input_tokens": True}])
def test_resposta_invalida_nao_grava(cenario, monkeypatch, resposta):
    gerar, _, _ = cenario
    monkeypatch.setattr(gerar, "post", lambda *args: resposta)
    assert contador.main() == 1
    assert not gerar.OUT_API.exists()
    assert not gerar.caminho_contagem("claude").exists()


def test_falha_no_meio_nao_grava_parcial(cenario, monkeypatch):
    gerar, _, chamadas = cenario

    def post(*args):
        chamadas.append(args)
        if len(chamadas) == 7:
            raise RuntimeError("HTTP 429")
        return {"input_tokens": 10}

    monkeypatch.setattr(gerar, "post", post)
    assert contador.main() == 1
    assert not gerar.OUT_API.exists()
    assert not gerar.caminho_contagem("claude").exists()


def test_chave_invalida_nao_e_repetida_no_erro(cenario, monkeypatch, capsys):
    _, _, chamadas = cenario
    monkeypatch.setenv("ANTHROPIC_API_KEY", "segredo\ncom-quebra")
    assert contador.main() == 1
    assert "segredo" not in capsys.readouterr().err
    assert chamadas == []


def test_usage_tem_precedencia(cenario):
    gerar, relatorio, _ = cenario
    assert contador.main() == 0
    claude = next(modelo for modelo in relatorio["modelos"] if modelo["id"] == "claude")
    claude["status"] = "medido"
    claude["resumo"] = {
        "tokens_en": 200,
        "tokens_pt": 220,
        "razao_pt_en": 1.1,
        "razao_origem": "usage",
    }
    tabela = gerar.markdown_api(relatorio, gerar.ler_contagens())
    assert "| 200 | 220 | 1,100 | usage |" in tabela
    assert "count_tokens" not in tabela


@pytest.mark.parametrize("campo", ["model", "dataset_sha256"])
def test_contagem_de_outro_modelo_ou_dataset_e_ignorada(cenario, campo):
    gerar, _, _ = cenario
    assert contador.main() == 0
    salvo = json.loads(gerar.caminho_contagem("claude").read_text(encoding="utf-8"))
    salvo[campo] = "outro"
    gerar.caminho_contagem("claude").write_text(json.dumps(salvo), encoding="utf-8")
    assert gerar.ler_contagens() == {}


def test_sem_contagem_a_tabela_fica_como_antes(cenario):
    gerar, relatorio, _ = cenario
    tabela = gerar.markdown_api(relatorio, gerar.ler_contagens())
    assert tabela.count("sem usage da API") == 4
    assert "count_tokens" not in tabela
