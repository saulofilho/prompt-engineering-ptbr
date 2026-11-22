"""Testa a contagem do Gemini sem rede: só countTokens, chave só pelo prompt."""

from __future__ import annotations

import json

import pytest
from conftest import ROOT, carregar

pytest.importorskip("tiktoken")
contador = carregar(ROOT / "poc" / "06_contar_tokens_claude.py", "contar_tokens_gemini")

CHAVE = "segredo-do-prompt"


@pytest.fixture
def cenario(tmp_path, monkeypatch):
    gerar = carregar(ROOT / "poc" / "04_gerar_e_avaliar.py", "gerar_para_gemini")
    poc = carregar(ROOT / "poc" / "01_tokenizacao.py", "poc_para_gemini")
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
    monkeypatch.setattr(contador.time, "sleep", lambda segundos: None)
    monkeypatch.setattr(contador.sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(contador.getpass, "getpass", lambda texto: CHAVE)
    monkeypatch.setenv("GEMINI_API_KEY", "chave-do-ambiente")
    monkeypatch.setenv("GOOGLE_API_KEY", "chave-do-ambiente")
    chamadas = []

    def post(*args):
        chamadas.append(args)
        return {"totalTokens": 12 if len(chamadas) % 2 == 0 else 10}

    monkeypatch.setattr(gerar, "post", post)
    return gerar, relatorio, chamadas


def test_so_chama_count_tokens_com_a_chave_do_prompt(cenario):
    _, _, chamadas = cenario
    assert contador.main("gemini") == 0
    assert len(chamadas) == 24
    for url, payload, headers in chamadas:
        assert url.endswith("/models/gemini-3.8-flash:countTokens")
        assert set(payload) == {"contents"}
        assert headers["x-goog-api-key"] == CHAVE


def test_preenche_so_o_gemini(cenario):
    gerar, _, _ = cenario
    assert contador.main("gemini") == 0
    tabela = gerar.OUT_API.read_text(encoding="utf-8")
    assert "| Gemini 3.8 Flash | 120 | 144 | 1,200 | countTokens" in tabela
    assert tabela.count("não medido") == 3
    assert "Anthropic" not in tabela
    assert CHAVE not in tabela + gerar.caminho_contagem("gemini").read_text(encoding="utf-8")


def test_convive_com_a_contagem_do_claude(cenario):
    gerar, relatorio, _ = cenario
    assert contador.main("gemini") == 0
    salvo = json.loads(gerar.caminho_contagem("gemini").read_text(encoding="utf-8"))
    claude = salvo | {"id": "claude", "model": "claude-haiku-4-5", "origem": "count_tokens"}
    gerar.caminho_contagem("claude").write_text(json.dumps(claude), encoding="utf-8")
    tabela = gerar.markdown_api(relatorio, gerar.ler_contagens())
    assert tabela.count("não medido") == 2


@pytest.mark.parametrize("quebra", [b"\n", b"\r\n"])
def test_quebra_de_linha_do_dataset_nao_invalida(cenario, monkeypatch, tmp_path, quebra):
    gerar, _, _ = cenario
    assert contador.main("gemini") == 0
    copia = tmp_path / "pares.json"
    copia.write_bytes(gerar.DATASET.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", quebra))
    monkeypatch.setattr(gerar, "DATASET", copia)
    assert "gemini" in gerar.ler_contagens()


def test_falha_nao_grava(cenario, monkeypatch):
    gerar, _, _ = cenario

    def post(*args):
        raise gerar.ErroAPI(429, "limite")

    monkeypatch.setattr(gerar, "post", post)
    assert contador.main("gemini") == 1
    assert not gerar.OUT_API.exists()
    assert not gerar.caminho_contagem("gemini").exists()
