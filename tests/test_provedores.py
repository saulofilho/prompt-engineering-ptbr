"""Testa o despacho por provedor em poc/04 com respostas mockadas.

Guarda contra mudança de schema das APIs: cada provedor extrai texto e
tokens de `usage` de um lugar diferente. Não faz chamada de rede.
"""

from __future__ import annotations

import pytest
from conftest import ROOT, carregar

gerar = carregar(ROOT / "poc" / "04_gerar_e_avaliar.py", "gerar_e_avaliar")

MENSAGENS = [{"role": "user", "content": "oi"}]

RESPOSTAS = {
    "openai": {
        "choices": [{"message": {"content": "resposta openai"}}],
        "usage": {"prompt_tokens": 11, "completion_tokens": 7},
    },
    "anthropic": {
        "content": [{"text": "resposta claude"}],
        "usage": {"input_tokens": 13, "output_tokens": 9},
    },
    "gemini": {
        "candidates": [{"content": {"parts": [{"text": "resposta gemini"}]}}],
        "usageMetadata": {"promptTokenCount": 17, "candidatesTokenCount": 5},
    },
}

ESPERADO = {
    "gpt-4o": ("resposta openai", 11, 7),
    "claude": ("resposta claude", 13, 9),
    "gemini": ("resposta gemini", 17, 5),
    "sabia": ("resposta openai", 11, 7),  # maritaca usa schema openai
}


@pytest.mark.parametrize("provedor", gerar.PROVEDORES, ids=lambda p: p["id"])
def test_chamar_extrai_texto_e_tokens(provedor, monkeypatch):
    resposta = RESPOSTAS[provedor["tipo"]]
    monkeypatch.setattr(gerar, "post", lambda url, payload, headers: resposta)
    texto, entrada, saida = gerar.chamar(provedor, MENSAGENS, "segredo-teste")
    assert (texto, entrada, saida) == ESPERADO[provedor["id"]]


def test_usd_de_none_quando_falta_token():
    assert gerar.usd_de(None, 1.0) is None
    assert gerar.usd_de(100, None) is None
    assert gerar.usd_de(1_000_000, 2.5) == pytest.approx(2.5)
