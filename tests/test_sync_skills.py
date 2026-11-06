"""Garante que .cursor/skills não divergiu de skills/."""

from __future__ import annotations

from conftest import ROOT, carregar

sync = carregar(ROOT / "tools" / "sync_skills.py", "sync_skills")


def test_cursor_skills_em_dia():
    erros = sync.divergencias()
    assert erros == [], "rode: python3 tools/sync_skills.py\n" + "\n".join(erros)
