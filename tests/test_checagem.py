"""Testes da checagem automática da rubrica v0.

Formaliza como pytest o que o script já afirmava em `_checar()`, mais alguns
casos de borda de formato e alucinação.
"""

from __future__ import annotations

from conftest import ROOT, carregar

checagem = carregar(ROOT / "evaluation" / "automatico" / "checagem_v0.py", "checagem_v0")
REGRAS = checagem.carregar_gabarito()


def avaliar(item_id: str, resposta: str, braco: str):
    return checagem.avaliar(item_id, resposta, braco, REGRAS)


def test_autochecagem_embutida_passa():
    # Não deve lançar; reexecuta as asserções originais do script.
    checagem._checar()


def test_ausencia_correta_nao_e_alucinacao():
    r = avaliar("qa-abertura", "não informado", "pt_otimizado")
    assert r["alucinacao"] is False
    assert r["ausencia"] == 2


def test_afirmar_quando_fonte_nao_informa_e_alucinacao():
    r = avaliar("qa-abertura", "A loja abre normalmente nesse feriado.", "pt_vago")
    assert r["alucinacao"] is True
    assert r["ausencia"] == 0


def test_lista_no_formato_pontua_cheio():
    r = avaliar(
        "resumo-chamados",
        "\n".join(
            [
                "- A equipe registrou 128 chamados na semana.",
                "- Quarenta por cento foram atraso de entrega.",
                "- Vinte e cinco por cento foram cobrança em duplicidade.",
                "- Quinze por cento foram falha de acesso.",
                "- A primeira resposta levou 6 horas, acima da meta de 2.",
            ]
        ),
        "pt_otimizado",
    )
    assert r["formato"] == 2
    assert r["alucinacao"] is False


def test_numero_fora_da_fonte_e_alucinacao():
    r = avaliar(
        "resumo-chamados",
        "- Houve 999 chamados de um tipo que o texto não cita e muda o quadro inteiro.",
        "pt_vago",
    )
    assert r["alucinacao"] is True


def test_nota_none_quando_fidelidade_indefinida():
    # json_objeto sem bloco JSON => fidelidade 0, não None; garante que nota soma.
    r = avaliar("extrair-chamado", "não consegui", "pt_vago")
    assert r["nota"] is not None


def test_gabarito_cobre_todos_os_ids_do_dataset():
    import json

    dataset = json.loads(
        (ROOT / "benchmarks" / "datasets" / "pares_v0.json").read_text(encoding="utf-8")
    )
    ids_dataset = {item["id"] for item in dataset["itens"]}
    assert ids_dataset <= set(REGRAS), ids_dataset - set(REGRAS)
