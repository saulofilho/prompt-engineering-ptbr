#!/usr/bin/env python3
"""Checagem automática da rubrica v0.

Não substitui avaliador humano. Mede formato, critério explícito,
fidelidade quando há gabarito e um sinal de alucinação verificável.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

GABARITO = Path(__file__).with_name("gabarito_v0.json")

PALAVRAS_PT = {
    "de", "que", "não", "nao", "para", "com", "uma", "em", "do", "da",
    "os", "as", "se", "por", "mais", "texto", "resposta", "prazo",
}
PALAVRAS_EN = {"the", "and", "with", "from", "this", "that", "each", "write", "using", "only"}


def carregar_gabarito() -> dict:
    return json.loads(GABARITO.read_text(encoding="utf-8"))["itens"]


def sem_cerca(texto: str) -> str:
    texto = texto.strip()
    texto = re.sub(r"^```(?:json|python)?\s*", "", texto)
    texto = re.sub(r"\s*```$", "", texto)
    return texto.strip()


def bloco_json(texto: str):
    limpo = sem_cerca(texto)
    inicio_obj = limpo.find("{")
    inicio_lista = limpo.find("[")
    if inicio_obj < 0 and inicio_lista < 0:
        return None
    if inicio_lista >= 0 and (inicio_obj < 0 or inicio_lista < inicio_obj):
        inicio = inicio_lista
        fim = limpo.rfind("]")
    else:
        inicio = inicio_obj
        fim = limpo.rfind("}")
    if fim <= inicio:
        return None
    try:
        return json.loads(limpo[inicio : fim + 1])
    except json.JSONDecodeError:
        return None


def itens_lista(texto: str) -> list[str]:
    achados = []
    for linha in texto.splitlines():
        linha = linha.strip()
        if re.match(r"^(?:[-*•]|\d+[.)])\s+\S", linha):
            achados.append(re.sub(r"^(?:[-*•]|\d+[.)])\s+", "", linha))
    return achados


def frases(texto: str) -> list[str]:
    partes = re.split(r"(?<=[.!?])\s+", sem_cerca(texto).replace("\n", " "))
    return [parte.strip() for parte in partes if parte.strip()]


def numeros(texto: str) -> set[int]:
    limpo = re.sub(r"(?m)^\s*\d+[.)]\s+", "", texto)
    limpo = limpo.replace(".", "").replace(",", "")
    return {int(valor) for valor in re.findall(r"\d+", limpo)}


def nome_do_braco(regra: dict, braco: str) -> str:
    nomes = regra["nomes"]
    if braco == "en":
        return nomes["en"]
    return nomes["pt"]


def idioma(texto: str, formato: str) -> int:
    if formato == "codigo":
        return 2
    tokens = re.findall(r"[A-Za-zÀ-ÿ]+", texto.lower())
    if not tokens:
        return 0
    pt = sum(token in PALAVRAS_PT or any(c in "áàãâéêíóôõúç" for c in token) for token in tokens)
    en = sum(token in PALAVRAS_EN for token in tokens)
    if pt == 0 and en == 0:
        return 1
    if pt > 0 and en > pt:
        return 1
    if pt == 0 and en > 0:
        return 0
    return 2


def nota_de(formato: int, criterios: int, fidelidade: int | None, ausencia: int, lingua: int) -> int | None:
    if fidelidade is None:
        return None
    return formato + criterios + fidelidade + ausencia + lingua


def avaliar(item_id: str, resposta: str, braco: str, gabarito: dict | None = None) -> dict:
    regras = gabarito if gabarito is not None else carregar_gabarito()
    regra = regras[item_id]
    texto = sem_cerca(resposta)
    formato = regra["formato"]
    alucinacao = False
    motivos: list[str] = []
    fidelidade: int | None = 2
    ausencia = 2
    criterios = 0
    formato_nota = 0

    if formato == "lista":
        itens = itens_lista(texto)
        formato_nota = 2 if len(itens) == regra["n_itens"] else (1 if itens else 0)
        dentro = [item for item in itens if len(item.split()) <= regra["max_palavras_item"]]
        if itens and len(itens) == regra["n_itens"] and len(dentro) == len(itens):
            criterios = 2
        elif itens and (len(itens) == regra["n_itens"] or len(dentro) == len(itens)):
            criterios = 1
        extras = numeros(texto) - set(regra["numeros_permitidos"])
        if extras:
            alucinacao = True
            fidelidade = 0
            motivos.append(f"número fora da fonte: {sorted(extras)}")
        elif formato_nota == 0:
            fidelidade = 1
    elif formato == "frases":
        achadas = frases(texto)
        formato_nota = 2 if len(achadas) == regra["n_itens"] else (1 if achadas else 0)
        dentro = [frase for frase in achadas if len(frase.split()) <= regra["max_palavras_item"]]
        if achadas and len(achadas) == regra["n_itens"] and len(dentro) == len(achadas):
            criterios = 2
        elif achadas:
            criterios = 1
        extras = numeros(texto) - set(regra["numeros_permitidos"])
        if extras:
            alucinacao = True
            fidelidade = 0
            motivos.append(f"número fora da fonte: {sorted(extras)}")
    elif formato == "json_objeto":
        dados = bloco_json(texto)
        if not isinstance(dados, dict):
            formato_nota = 1 if "{" in texto else 0
            criterios = 0
            fidelidade = 0
            alucinacao = "{" in texto
        else:
            presentes = [campo for campo in regra["campos"] if campo in dados]
            formato_nota = 2 if presentes == regra["campos"] and set(dados) <= set(regra["campos"]) else 1
            criterios = 2 if presentes == regra["campos"] else (1 if presentes else 0)
            texto_dados = json.dumps(dados, ensure_ascii=False)
            faltas = [
                campo
                for campo, trecho in regra.get("contem", {}).items()
                if trecho.lower() not in texto_dados.lower() and trecho.replace(".", "") not in texto_dados.replace(".", "")
            ]
            if faltas:
                fidelidade = 1 if len(faltas) < len(regra["contem"]) else 0
                motivos.append(f"campo divergente: {faltas}")
            if formato_nota < 2 and re.search(r"\d{3,}", texto) and not regra.get("contem"):
                alucinacao = True
    elif formato == "json_lista":
        dados = bloco_json(texto)
        if not isinstance(dados, list):
            formato_nota = 1 if "[" in texto else 0
            fidelidade = 0
        else:
            campo = regra["campo_classe"]
            classes = []
            for item in dados:
                if isinstance(item, dict) and campo in item:
                    classes.append(str(item[campo]))
            formato_nota = 2 if len(dados) == regra["n_itens"] and len(classes) == regra["n_itens"] else 1
            validas = [classe for classe in classes if classe in regra["classes"]]
            criterios = 2 if len(validas) == regra["n_itens"] else (1 if validas else 0)
            esperadas = regra.get("classes_esperadas")
            if esperadas and classes != esperadas:
                fidelidade = 1
                motivos.append(f"classes {classes} diferentes do gabarito {esperadas}")
            elif not esperadas:
                fidelidade = 2
    elif formato == "codigo":
        nome = nome_do_braco(regra, braco)
        tem_nome = nome in texto
        exige = all(trecho in texto for trecho in regra.get("exige", []))
        linhas = [linha for linha in texto.splitlines() if linha.strip()]
        prosa = sum(1 for linha in linhas if not linha.strip().startswith(("#", "def ", "class ", " ", "\t", "import", "from", "return", "assert", "@")))
        formato_nota = 2 if tem_nome and exige and prosa <= 2 else (1 if tem_nome else 0)
        criterios = 2 if tem_nome and exige else (1 if tem_nome or exige else 0)
        if "import os" in texto or "subprocess" in texto or "socket" in texto:
            alucinacao = True
            fidelidade = 0
            motivos.append("código pede recurso fora do enunciado")
    elif formato == "prosa":
        linhas = [linha for linha in texto.splitlines() if linha.strip()]
        formato_nota = 2 if linhas and len(linhas) <= regra["max_linhas"] else (1 if linhas else 0)
        criterios = 2 if formato_nota == 2 else (1 if linhas else 0)
        escolhe_a = re.search(r"(?:escolh\w+|fornecedor)\s+A\b", texto, re.I)
        escolhe_b = re.search(r"(?:escolh\w+|fornecedor)\s+B\b", texto, re.I)
        if escolhe_a and not escolhe_b:
            fidelidade = 2
        elif escolhe_b and not escolhe_a:
            fidelidade = 0
            alucinacao = True
            motivos.append("escolha diferente do gabarito A")
        else:
            fidelidade = 1
        extras = numeros(texto) - set(regra["numeros_permitidos"])
        if extras:
            alucinacao = True
            fidelidade = 0
            motivos.append(f"número fora da fonte: {sorted(extras)}")
    elif formato == "frase":
        uma = len(frases(texto)) <= 2 and len(texto.splitlines()) <= 3
        formato_nota = 2 if uma and texto else 1 if texto else 0
        criterios = formato_nota
        if "exato" in regra:
            alvo = regra["exato"].lower()
            normal = texto.lower().strip().strip(".")
            if normal == alvo or normal.startswith(alvo):
                fidelidade = 2
                ausencia = 2
            elif alvo in normal and len(normal) < 80:
                fidelidade = 1
                ausencia = 2
            else:
                fidelidade = 0
                ausencia = 0
                alucinacao = True
                motivos.append("afirmou conteúdo quando a fonte não informa")
        elif "contem" in regra:
            if regra["contem"].lower() in texto.lower():
                fidelidade = 2
                if regra.get("proibe_so_ausencia") and texto.lower().strip().strip(".") == "não informado":
                    fidelidade = 0
                    alucinacao = True
            else:
                fidelidade = 0
                alucinacao = "não informado" in texto.lower() or True
                motivos.append("resposta não contém o fato verificável")
        if "contem_numero" in regra:
            resposta_numeros = numeros(texto)
            if regra["contem_numero"] in resposta_numeros:
                fidelidade = 2
                if regra.get("proibe_numero_como_resposta") in resposta_numeros and regra["contem_numero"] not in resposta_numeros:
                    fidelidade = 0
            else:
                fidelidade = 0
                alucinacao = True
                if regra.get("proibe_numero_como_resposta") in resposta_numeros:
                    motivos.append("usou o valor de outro plano")
                else:
                    motivos.append("valor diferente do texto")

    lingua = idioma(texto, formato)
    return {
        "formato": formato_nota,
        "criterios": criterios,
        "fidelidade": fidelidade,
        "ausencia": ausencia,
        "idioma": lingua,
        "nota": nota_de(formato_nota, criterios, fidelidade, ausencia, lingua),
        "alucinacao": bool(alucinacao) if fidelidade is not None else False,
        "motivos": motivos,
        "formato_util": formato_nota == 2,
    }


def _checar() -> None:
    regras = carregar_gabarito()
    boa = avaliar(
        "qa-abertura",
        "não informado",
        "pt_otimizado",
        regras,
    )
    ruim = avaliar(
        "qa-abertura",
        "A loja abre normalmente nesse feriado.",
        "pt_vago",
        regras,
    )
    assert boa["alucinacao"] is False and boa["ausencia"] == 2, boa
    assert ruim["alucinacao"] is True and ruim["ausencia"] == 0, ruim
    lista = avaliar(
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
        regras,
    )
    assert lista["formato"] == 2, lista
    inventado = avaliar(
        "resumo-chamados",
        "- Houve 999 chamados de um tipo que o texto não cita e isso muda o quadro inteiro do relatório semanal da equipe hoje.",
        "pt_vago",
        regras,
    )
    assert inventado["alucinacao"] is True, inventado
    print("checagem automática ok")


if __name__ == "__main__":
    _checar()
