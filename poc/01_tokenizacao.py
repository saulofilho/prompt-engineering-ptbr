#!/usr/bin/env python3
"""Piloto v0: conta tokens de prompts pareados.

Não chama API, não mede qualidade e não altera hipóteses.
A contagem de BPE não é aditiva: instrução e payload são medidos
à parte, e o prompt completo é medido de novo, já concatenado.
"""

from __future__ import annotations

import hashlib
import json
import sys
import unicodedata
from pathlib import Path

import tiktoken

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "benchmarks" / "datasets" / "pares_v0.json"
LEXICO = ROOT / "benchmarks" / "datasets" / "lexico_v0.json"
HIPOTESES = ROOT / "HIPOTESES.md"
OUT_JSON = ROOT / "benchmarks" / "results" / "poc_v0_tokenizacao.json"
OUT_MD = ROOT / "benchmarks" / "results" / "poc_v0_tokenizacao.md"

ENCODINGS = ("o200k_base", "cl100k_base")
PRIMARIO = "o200k_base"
BRACOS = ("en", "pt_paralelo", "pt_coloquial", "pt_vago", "pt_otimizado")
ROTULOS = {
    "en": "EN",
    "pt_paralelo": "PT paralelo",
    "pt_coloquial": "PT coloquial",
    "pt_vago": "PT vago",
    "pt_otimizado": "PT otimizado",
    "pt_sem_acento": "PT sem diacrítico",
}


def sha256_arquivo(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def nfc(texto: str) -> str:
    return unicodedata.normalize("NFC", texto)


def sem_diacriticos(texto: str) -> str:
    normalizado = unicodedata.normalize("NFKD", nfc(texto))
    return "".join(caractere for caractere in normalizado if not unicodedata.combining(caractere))


def validar_marcadores(conjunto: dict) -> list[str]:
    erros: list[str] = []
    for item in conjunto["itens"]:
        for braco in ("pt_paralelo", "pt_coloquial", "pt_otimizado"):
            texto = item["instrucao"][braco]
            for marcador in item["marcadores_pt"]:
                if marcador not in texto:
                    erros.append(f"{item['id']} {braco} sem marcador {marcador!r}")
        for marcador in item["marcadores_en"]:
            if marcador not in item["instrucao"]["en"]:
                erros.append(f"{item['id']} en sem marcador {marcador!r}")
        vago = item["instrucao"]["pt_vago"]
        presentes = [marcador for marcador in item["marcadores_pt"] if marcador in vago]
        if len(presentes) == len(item["marcadores_pt"]):
            erros.append(f"{item['id']} pt_vago contém todos os marcadores")
    return erros


def medidas(texto: str, codificador) -> dict:
    texto = nfc(texto)
    identificadores = codificador.encode(texto, disallowed_special=())
    palavras = texto.split()
    caracteres = len(texto)
    tokens = len(identificadores)
    return {
        "tokens": tokens,
        "palavras": len(palavras),
        "caracteres": caracteres,
        "bytes_utf8": len(texto.encode("utf-8")),
        "tokens_por_palavra": (tokens / len(palavras)) if palavras else None,
        "caracteres_por_token": (caracteres / tokens) if tokens else None,
    }


def montar_completo(instrucao: str, rotulo: str, fonte: str) -> str:
    return f"{nfc(instrucao)}\n\n{nfc(rotulo)}\n{nfc(fonte)}"


def pecas(codificador, texto: str) -> list[str]:
    identificadores = codificador.encode(nfc(texto), disallowed_special=())
    return [
        codificador.decode_single_token_bytes(identificador).decode("utf-8", errors="replace")
        for identificador in identificadores
    ]


def somar(linhas: list[dict], braco: str, escopo: str) -> dict:
    tokens = sum(linha[braco][escopo]["tokens"] for linha in linhas)
    palavras = sum(linha[braco][escopo]["palavras"] for linha in linhas)
    caracteres = sum(linha[braco][escopo]["caracteres"] for linha in linhas)
    return {
        "tokens": tokens,
        "palavras": palavras,
        "caracteres": caracteres,
        "tokens_por_palavra": (tokens / palavras) if palavras else None,
        "caracteres_por_token": (caracteres / tokens) if tokens else None,
    }


def razao(numerador: int, denominador: int) -> float | None:
    if denominador == 0:
        return None
    return numerador / denominador


def fmt(valor: float | None, casas: int = 3) -> str:
    if valor is None:
        return "—"
    return f"{valor:.{casas}f}".replace(".", ",")


def fmt_pct(valor: float | None) -> str:
    if valor is None:
        return "—"
    return f"{valor * 100:.1f}".replace(".", ",") + "%"


def decidir_h1(reducao: float | None) -> str:
    if reducao is None:
        return "inconclusiva"
    if reducao >= 0.15:
        return "compativel com H1 neste conjunto"
    return "nao confirma H1 neste conjunto"


def decidir_h3(premio: float | None) -> str:
    if premio is None:
        return "inconclusiva"
    if premio > 1:
        return "compativel com H3 neste conjunto"
    return "nao confirma H3 neste conjunto"


def decidir_h5(reducao: float | None) -> str:
    if reducao is None:
        return "inconclusiva"
    if reducao >= 0.02:
        return "recusa H5 neste conjunto"
    return "compativel com H5 neste conjunto"


def contraste(linhas: list[dict], esquerda: str, direita: str, escopo: str) -> dict:
    soma_esquerda = somar(linhas, esquerda, escopo)
    soma_direita = somar(linhas, direita, escopo)
    premio = razao(soma_esquerda["tokens"], soma_direita["tokens"])
    reducao = None if premio is None else 1 - premio
    premio_caracteres = razao(soma_esquerda["caracteres"], soma_direita["caracteres"])
    premio_palavras = razao(soma_esquerda["palavras"], soma_direita["palavras"])
    alem_do_comprimento = None
    if premio is not None and premio_caracteres not in (None, 0):
        alem_do_comprimento = premio / premio_caracteres
    return {
        "escopo": escopo,
        "tokens_esquerda": soma_esquerda["tokens"],
        "tokens_direita": soma_direita["tokens"],
        "razao_tokens": premio,
        "reducao": reducao,
        "razao_caracteres": premio_caracteres,
        "razao_palavras": premio_palavras,
        "razao_tokens_sobre_razao_caracteres": alem_do_comprimento,
    }


def carregar_codificadores() -> dict:
    codificadores = {}
    for nome in ENCODINGS:
        codificadores[nome] = tiktoken.get_encoding(nome)
    return codificadores


def medir_encoding(conjunto: dict, nome: str, codificador) -> dict:
    linhas = []
    for item in conjunto["itens"]:
        registro = {"id": item["id"], "tarefa": item["tarefa"]}
        for braco in BRACOS:
            rotulo = item["rotulo_en"] if braco == "en" else item["rotulo_pt"]
            fonte = item["fonte_en"] if braco == "en" else item["fonte_pt"]
            instrucao = item["instrucao"][braco]
            payload = f"{nfc(rotulo)}\n{nfc(fonte)}"
            completo = montar_completo(instrucao, rotulo, fonte)
            registro[braco] = {
                "instrucao": medidas(instrucao, codificador),
                "payload": medidas(payload, codificador),
                "completo": medidas(completo, codificador),
            }
        otimizado = registro["pt_otimizado"]
        instrucao_otimizada = item["instrucao"]["pt_otimizado"]
        rotulo = item["rotulo_pt"]
        fonte = item["fonte_pt"]
        completo_otimizado = montar_completo(instrucao_otimizada, rotulo, fonte)
        registro["pt_sem_acento"] = {
            "instrucao": medidas(sem_diacriticos(instrucao_otimizada), codificador),
            "payload": medidas(sem_diacriticos(f"{rotulo}\n{fonte}"), codificador),
            "completo": medidas(sem_diacriticos(completo_otimizado), codificador),
        }
        registro["pt_otimizado_referencia_tokens_completo"] = otimizado["completo"]["tokens"]
        linhas.append(registro)

    h1 = contraste(linhas, "pt_otimizado", "pt_coloquial", "instrucao")
    h1_completo = contraste(linhas, "pt_otimizado", "pt_coloquial", "completo")
    h3 = contraste(linhas, "pt_paralelo", "en", "completo")
    h3_instrucao = contraste(linhas, "pt_paralelo", "en", "instrucao")
    h5 = contraste(linhas, "pt_sem_acento", "pt_otimizado", "completo")
    vago = contraste(linhas, "pt_vago", "pt_otimizado", "instrucao")

    return {
        "encoding": nome,
        "itens": linhas,
        "somas": {
            braco: {
                escopo: somar(linhas, braco, escopo)
                for escopo in ("instrucao", "payload", "completo")
            }
            for braco in (*BRACOS, "pt_sem_acento")
        },
        "contrastes": {
            "h1_instrucao": h1,
            "h1_completo": h1_completo,
            "h3_completo": h3,
            "h3_instrucao": h3_instrucao,
            "h5_completo": h5,
            "vago_contra_otimizado_instrucao": vago,
        },
        "decisao": {
            "h1": decidir_h1(h1["reducao"]),
            "h3": decidir_h3(h3["razao_tokens"]),
            "h5": decidir_h5(h5["reducao"]),
        },
    }


def medir_lexico(lexico: dict, codificadores: dict) -> dict:
    saida = {}
    for nome, codificador in codificadores.items():
        pares = []
        for par in lexico["pares"]:
            com = nfc(par["com_diacritico"])
            sem = nfc(par["sem_diacritico"])
            pares.append(
                {
                    "id": par["id"],
                    "com_diacritico": {
                        "forma": com,
                        "isolada": pecas(codificador, com),
                        "com_espaco": pecas(codificador, f" {com}"),
                    },
                    "sem_diacritico": {
                        "forma": sem,
                        "isolada": pecas(codificador, sem),
                        "com_espaco": pecas(codificador, f" {sem}"),
                    },
                }
            )
        formas = []
        for forma in lexico["formas"]:
            forma = nfc(forma)
            formas.append(
                {
                    "forma": forma,
                    "isolada": pecas(codificador, forma),
                    "com_espaco": pecas(codificador, f" {forma}"),
                }
            )
        saida[nome] = {"pares": pares, "formas": formas}
    return saida


def tabela_somas(medicao: dict) -> list[str]:
    linhas = [
        "| Braço | Instrução | Payload | Completo | Palavras | Caracteres | Tokens/palavra | Caracteres/token |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for braco in (*BRACOS, "pt_sem_acento"):
        completo = medicao["somas"][braco]["completo"]
        linhas.append(
            "| {rotulo} | {inst} | {pay} | {comp} | {pal} | {car} | {tp} | {ct} |".format(
                rotulo=ROTULOS[braco],
                inst=medicao["somas"][braco]["instrucao"]["tokens"],
                pay=medicao["somas"][braco]["payload"]["tokens"],
                comp=completo["tokens"],
                pal=completo["palavras"],
                car=completo["caracteres"],
                tp=fmt(completo["tokens_por_palavra"], 2),
                ct=fmt(completo["caracteres_por_token"], 2),
            )
        )
    return linhas


def linha_contraste(nome: str, bloco: dict) -> str:
    return (
        f"| {nome} | {bloco['escopo']} | {bloco['tokens_esquerda']} | {bloco['tokens_direita']} | "
        f"{fmt(bloco['razao_tokens'])} | {fmt_pct(bloco['reducao'])} | "
        f"{fmt(bloco['razao_caracteres'])} | {fmt(bloco['razao_tokens_sobre_razao_caracteres'])} |"
    )


def tabela_itens(medicao: dict) -> list[str]:
    linhas = [
        "| Tarefa | Coloquial | Otimizado | Redução | Paralelo | EN | Vago | Sem diacrítico |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for item in medicao["itens"]:
        coloquial = item["pt_coloquial"]["instrucao"]["tokens"]
        otimizado = item["pt_otimizado"]["instrucao"]["tokens"]
        reducao = 1 - (otimizado / coloquial) if coloquial else None
        linhas.append(
            "| {id} | {col} | {oti} | {red} | {par} | {en} | {vago} | {sem} |".format(
                id=item["id"],
                col=coloquial,
                oti=otimizado,
                red=fmt_pct(reducao),
                par=item["pt_paralelo"]["instrucao"]["tokens"],
                en=item["en"]["instrucao"]["tokens"],
                vago=item["pt_vago"]["instrucao"]["tokens"],
                sem=item["pt_sem_acento"]["completo"]["tokens"],
            )
        )
    return linhas


def tabela_lexico(lexico_medido: dict) -> list[str]:
    linhas = [
        "| Forma | o200k isolada | o200k com espaço | cl100k isolada | cl100k com espaço |",
        "| --- | --- | --- | --- | --- |",
    ]
    o200 = lexico_medido[PRIMARIO]
    cl100 = lexico_medido["cl100k_base"]
    for indice, par in enumerate(o200["pares"]):
        outro = cl100["pares"][indice]
        for chave in ("com_diacritico", "sem_diacritico"):
            linhas.append(
                "| `{forma}` | {a} | {b} | {c} | {d} |".format(
                    forma=par[chave]["forma"],
                    a=" · ".join(par[chave]["isolada"]),
                    b=" · ".join(par[chave]["com_espaco"]),
                    c=" · ".join(outro[chave]["isolada"]),
                    d=" · ".join(outro[chave]["com_espaco"]),
                )
            )
    for indice, forma in enumerate(o200["formas"]):
        outro = cl100["formas"][indice]
        linhas.append(
            "| `{forma}` | {a} | {b} | {c} | {d} |".format(
                forma=forma["forma"],
                a=" · ".join(forma["isolada"]),
                b=" · ".join(forma["com_espaco"]),
                c=" · ".join(outro["isolada"]),
                d=" · ".join(outro["com_espaco"]),
            )
        )
    return linhas


def markdown(relatorio: dict) -> str:
    primario = relatorio["medicoes"][PRIMARIO]
    secundario = relatorio["medicoes"]["cl100k_base"]
    partes = [
        "# Piloto v0 — contagem de tokens",
        "",
        "Resultado gerado por `poc/01_tokenizacao.py`. Não edite este arquivo à mão: rode o script de novo.",
        "",
        "Este piloto descreve o conjunto v0. Não é estimativa populacional, não tem teste de hipótese confirmatório e não mede qualidade de resposta.",
        "",
        f"- Dataset: `{relatorio['dataset_sha256']}`",
        f"- Hipóteses: `{relatorio['hipoteses_sha256']}`",
        f"- Léxico: `{relatorio['lexico_sha256']}`",
        f"- Itens: {relatorio['n_itens']}",
        f"- Encoding da decisão: `{PRIMARIO}`",
        "",
        "A soma de instrução e payload não precisa fechar com o prompt completo. O tokenizador de subpalavras pode fundir ou cortar a fronteira quando os trechos são concatenados. Cada escopo foi contado no texto que de fato o representa.",
        "",
        "## Decisão no conjunto, encoding primário",
        "",
        f"- H1, instrução, redução de `pt_otimizado` frente a `pt_coloquial`: {fmt_pct(primario['contrastes']['h1_instrucao']['reducao'])}. {primario['decisao']['h1']}.",
        f"- H3, prompt completo, razão `pt_paralelo` / `en`: {fmt(primario['contrastes']['h3_completo']['razao_tokens'])}. {primario['decisao']['h3']}.",
        f"- H5, prompt completo, redução ao remover diacríticos: {fmt_pct(primario['contrastes']['h5_completo']['reducao'])}. {primario['decisao']['h5']}.",
        "",
        "H2 e H4 não foram testadas. `pt_vago` pode gastar menos tokens porque apaga critérios; isso não é economia útil.",
        "",
        f"## Somas — {PRIMARIO}",
        "",
        *tabela_somas(primario),
        "",
        f"## Contrastes — {PRIMARIO}",
        "",
        "A coluna da esquerda é o primeiro braço do contraste. Redução positiva significa que a esquerda gastou menos tokens que a direita.",
        "",
        "| Contraste | Escopo | Tokens à esquerda | Tokens à direita | Razão | Redução | Razão de caracteres | Tokens além do comprimento |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        linha_contraste("otimizado / coloquial", primario["contrastes"]["h1_instrucao"]),
        linha_contraste("otimizado / coloquial", primario["contrastes"]["h1_completo"]),
        linha_contraste("paralelo / en", primario["contrastes"]["h3_instrucao"]),
        linha_contraste("paralelo / en", primario["contrastes"]["h3_completo"]),
        linha_contraste("sem diacrítico / otimizado", primario["contrastes"]["h5_completo"]),
        linha_contraste("vago / otimizado", primario["contrastes"]["vago_contra_otimizado_instrucao"]),
        "",
        "“Tokens além do comprimento” é a razão de tokens dividida pela razão de caracteres. Valor perto de 1 indica que a diferença de tokens acompanha o tamanho do texto. Valor acima de 1 indica fragmentação adicional.",
        "",
        f"## Instruções por tarefa — {PRIMARIO}",
        "",
        "A redução é da instrução otimizada frente à coloquial. A coluna “Sem diacrítico” é o prompt completo, não a instrução.",
        "",
        *tabela_itens(primario),
        "",
        f"## Somas — cl100k_base",
        "",
        *tabela_somas(secundario),
        "",
        "## Contrastes — cl100k_base",
        "",
        "Secundário. Não decide H1, H3 nem H5.",
        "",
        "| Contraste | Escopo | Tokens à esquerda | Tokens à direita | Razão | Redução | Razão de caracteres | Tokens além do comprimento |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        linha_contraste("otimizado / coloquial", secundario["contrastes"]["h1_instrucao"]),
        linha_contraste("otimizado / coloquial", secundario["contrastes"]["h1_completo"]),
        linha_contraste("paralelo / en", secundario["contrastes"]["h3_instrucao"]),
        linha_contraste("paralelo / en", secundario["contrastes"]["h3_completo"]),
        linha_contraste("sem diacrítico / otimizado", secundario["contrastes"]["h5_completo"]),
        linha_contraste("vago / otimizado", secundario["contrastes"]["vago_contra_otimizado_instrucao"]),
        "",
        "## Fragmentação de formas",
        "",
        "Cada célula lista as peças, separadas por `·`. “Com espaço” é a forma no meio de uma frase, com o espaço que o pré-tokenizador costuma colar na palavra. A grafia sem diacrítico está aqui para ser observada. Não é modelo de escrita.",
        "",
        *tabela_lexico(relatorio["lexico"]),
        "",
        "## Leitura que este arquivo não autoriza",
        "",
        "- Não autoriza dizer que a ABNT economiza tokens.",
        "- Não autoriza remover acento como prática.",
        "- Não autoriza concluir que o prompt otimizado responde melhor. Qualidade não foi medida.",
        "- Não autoriza transportar o prêmio deste conjunto para outro corpus ou outro tokenizador.",
        "",
    ]
    return "\n".join(partes) + "\n"


def main() -> int:
    conjunto = json.loads(DATASET.read_text(encoding="utf-8"))
    lexico = json.loads(LEXICO.read_text(encoding="utf-8"))
    erros = validar_marcadores(conjunto)
    if erros:
        for erro in erros:
            print(erro, file=sys.stderr)
        return 1
    if "--checar" in sys.argv:
        print(f"marcadores ok ({len(conjunto['itens'])} itens)")
        return 0

    codificadores = carregar_codificadores()
    medicoes = {
        nome: medir_encoding(conjunto, nome, codificador)
        for nome, codificador in codificadores.items()
    }
    relatorio = {
        "versao": "v0",
        "n_itens": len(conjunto["itens"]),
        "dataset_sha256": sha256_arquivo(DATASET),
        "hipoteses_sha256": sha256_arquivo(HIPOTESES),
        "lexico_sha256": sha256_arquivo(LEXICO),
        "encoding_primario": PRIMARIO,
        "aviso": "Piloto descritivo. Sem qualidade, sem preço e sem generalização.",
        "medicoes": medicoes,
        "lexico": medir_lexico(lexico, codificadores),
    }
    OUT_JSON.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown(relatorio), encoding="utf-8")
    decisao = medicoes[PRIMARIO]["decisao"]
    h1 = medicoes[PRIMARIO]["contrastes"]["h1_instrucao"]["reducao"]
    h3 = medicoes[PRIMARIO]["contrastes"]["h3_completo"]["razao_tokens"]
    h5 = medicoes[PRIMARIO]["contrastes"]["h5_completo"]["reducao"]
    print(f"H1 reducao instrucao: {h1:.3f} — {decisao['h1']}")
    print(f"H3 premio completo: {h3:.3f} — {decisao['h3']}")
    print(f"H5 reducao sem diacritico: {h5:.3f} — {decisao['h5']}")
    print(f"escreveu {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
