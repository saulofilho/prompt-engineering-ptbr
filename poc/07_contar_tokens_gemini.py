#!/usr/bin/env python3
"""Conta a razão PT/EN do Gemini pelo countTokens, sem gerar resposta.

Pede sempre a chave no prompt oculto e ignora GEMINI_API_KEY e GOOGLE_API_KEY,
que podem ser de um projeto com faturamento. Nunca chama generateContent.
Use só com texto público: no nível gratuito, o Google pode ler o que é enviado.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

BASE = Path(__file__).resolve().with_name("06_contar_tokens_claude.py")


def main() -> int:
    spec = importlib.util.spec_from_file_location("contar_tokens", BASE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"não foi possível carregar {BASE}")
    contador = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(contador)
    return contador.main("gemini")


if __name__ == "__main__":
    raise SystemExit(main())
