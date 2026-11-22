"""poc/04 não pode levar chave para URL, arquivo versionado ou terminal. Sem rede."""

from __future__ import annotations

import io
import json
import sys
import urllib.error

import pytest
from conftest import ROOT, carregar

pytest.importorskip("tiktoken")
CHAVE = "segredo-ficticio-1234"
MALFORMADAS = [f"{CHAVE} colado", f"{CHAVE}\ncolado", f"{CHAVE}​colado"]
IDS = ["gpt-4o", "claude", "gemini", "sabia"]


@pytest.fixture
def gerar(tmp_path, monkeypatch):
    modulo = carregar(ROOT / "poc" / "04_gerar_e_avaliar.py", "gerar_segredos")
    for nome in ("OUT_JSON", "OUT_MD", "OUT_API"):
        monkeypatch.setattr(modulo, nome, tmp_path / getattr(modulo, nome).name)
    monkeypatch.setattr(sys, "argv", ["04"])
    for provedor in modulo.PROVEDORES:
        for nome in provedor["env"]:
            monkeypatch.delenv(nome, raising=False)
    return modulo


def rodar(gerar, monkeypatch, capsys, id_provedor, chave):
    provedor = next(p for p in gerar.PROVEDORES if p["id"] == id_provedor)
    monkeypatch.setenv(provedor["env"][0], chave)
    assert gerar.main() == 0
    saida = capsys.readouterr()
    arquivos = gerar.OUT_JSON.read_text() + gerar.OUT_MD.read_text() + gerar.OUT_API.read_text()
    return saida.out + saida.err, arquivos


@pytest.mark.parametrize("id_provedor", IDS)
@pytest.mark.parametrize("chave", MALFORMADAS)
def test_chave_malformada_nao_vaza(gerar, monkeypatch, capsys, id_provedor, chave):
    def rede(*args, **kwargs):
        # É o que o http.client faz com URL ou cabeçalho inválido: repete o valor.
        pedido = next(a for a in args if hasattr(a, "full_url"))
        raise ValueError(f"inválido: {pedido.full_url} {pedido.header_items()}")

    monkeypatch.setattr("urllib.request.OpenerDirector.open", rede)
    tela, arquivos = rodar(gerar, monkeypatch, capsys, id_provedor, chave)
    assert CHAVE not in tela
    assert CHAVE not in arquivos


@pytest.mark.parametrize("id_provedor", IDS)
def test_corpo_de_erro_do_provedor_nao_vai_para_arquivo(gerar, monkeypatch, capsys, id_provedor):
    def rede(*args, **kwargs):
        corpo = json.dumps({"error": f"chave {CHAVE} recusada, final ***1234"}).encode()
        raise urllib.error.HTTPError("https://x", 401, "erro", {}, io.BytesIO(corpo))

    monkeypatch.setattr("urllib.request.OpenerDirector.open", rede)
    tela, arquivos = rodar(gerar, monkeypatch, capsys, id_provedor, CHAVE)
    assert CHAVE not in tela
    assert "1234" not in arquivos
    assert "HTTP 401" in arquivos


def test_gemini_manda_chave_no_cabecalho(gerar, monkeypatch):
    pedidos = []

    def post(url, payload, headers):
        pedidos.append((url, headers))
        return {"candidates": [{"content": {"parts": [{"text": "ok"}]}}]}

    monkeypatch.setattr(gerar, "post", post)
    provedor = next(p for p in gerar.PROVEDORES if p["id"] == "gemini")
    gerar.chamar(provedor, [{"role": "user", "content": "oi"}], CHAVE)
    url, headers = pedidos[0]
    assert CHAVE not in url
    assert headers["x-goog-api-key"] == CHAVE


def test_nao_segue_redirecionamento(gerar):
    assert gerar.SemRedirecionamento().redirect_request(None, None, 302, "", {}, "https://outro") is None
