#!/usr/bin/env python3
"""Benchmark de tokens: português brasileiro paralelo contra inglês, por modelo.

Conta o mesmo par de prompts no tokenizador publicado de cada família.
Não chama o modelo, não mede qualidade e não preenche linha sem tokenizador.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOGO = ROOT / "benchmarks" / "datasets" / "modelos_v0.json"
DATASET = ROOT / "benchmarks" / "datasets" / "pares_v0.json"
OUT_JSON = ROOT / "benchmarks" / "results" / "benchmark_modelos_ptbr_en.json"
OUT_MD = ROOT / "benchmarks" / "results" / "benchmark_modelos_ptbr_en.md"


def carregar_poc():
    caminho = ROOT / "poc" / "01_tokenizacao.py"
    spec = importlib.util.spec_from_file_location("poc_tokenizacao", caminho)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"não foi possível carregar {caminho}")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def fmt(valor: float | None, casas: int = 3) -> str:
    if valor is None:
        return "—"
    return f"{valor:.{casas}f}".replace(".", ",")


def mediana(valores: list[float]) -> float | None:
    if not valores:
        return None
    ordenados = sorted(valores)
    meio = len(ordenados) // 2
    if len(ordenados) % 2:
        return ordenados[meio]
    return (ordenados[meio - 1] + ordenados[meio]) / 2


def textos(poc, item: dict, braco: str) -> tuple[str, str]:
    if braco == "en":
        rotulo = item["rotulo_en"]
        fonte = item["fonte_en"]
    else:
        rotulo = item["rotulo_pt"]
        fonte = item["fonte_pt"]
    instrucao = item["instrucao"][braco]
    return instrucao, poc.montar_completo(instrucao, rotulo, fonte)


def contador_de(modelo: dict):
    backend = modelo["backend"]
    if backend == "tiktoken":
        import tiktoken

        try:
            codificador = tiktoken.get_encoding(modelo["ref"])
        except Exception as exc:
            raise RuntimeError(f"encoding {modelo['ref']} indisponível neste tiktoken ({exc})") from exc

        def contar(texto: str, codificador=codificador) -> int:
            return len(codificador.encode(texto, disallowed_special=()))

        return contar

    if backend == "hf":
        from tokenizers import Tokenizer

        tokenizador = Tokenizer.from_pretrained(modelo["ref"])

        def contar(texto: str, tokenizador=tokenizador) -> int:
            return len(tokenizador.encode(texto, add_special_tokens=False).ids)

        return contar

    if backend == "nao-publicado":
        raise RuntimeError(modelo["nota"])

    raise RuntimeError(f"backend desconhecido: {backend}")


def medir_modelo(poc, itens: list[dict], contar) -> dict:
    por_item = []
    soma = {
        "en": {"instrucao": 0, "completo": 0, "caracteres": 0, "palavras": 0},
        "pt_paralelo": {"instrucao": 0, "completo": 0, "caracteres": 0, "palavras": 0},
    }
    for item in itens:
        linha = {"id": item["id"], "tarefa": item["tarefa"]}
        for braco in ("en", "pt_paralelo"):
            instrucao, completo = textos(poc, item, braco)
            instrucao = poc.nfc(instrucao)
            completo = poc.nfc(completo)
            tokens_instrucao = contar(instrucao)
            tokens_completo = contar(completo)
            linha[braco] = {
                "instrucao": tokens_instrucao,
                "completo": tokens_completo,
                "caracteres": len(completo),
                "palavras": len(completo.split()),
            }
            soma[braco]["instrucao"] += tokens_instrucao
            soma[braco]["completo"] += tokens_completo
            soma[braco]["caracteres"] += len(completo)
            soma[braco]["palavras"] += len(completo.split())
        razao = linha["pt_paralelo"]["completo"] / linha["en"]["completo"]
        linha["razao_completo"] = razao
        por_item.append(linha)

    razoes = [linha["razao_completo"] for linha in por_item]
    razao_completa = soma["pt_paralelo"]["completo"] / soma["en"]["completo"]
    razao_instrucao = soma["pt_paralelo"]["instrucao"] / soma["en"]["instrucao"]
    razao_caracteres = soma["pt_paralelo"]["caracteres"] / soma["en"]["caracteres"]
    return {
        "somas": soma,
        "razao_completo": razao_completa,
        "razao_instrucao": razao_instrucao,
        "razao_caracteres": razao_caracteres,
        "alem_do_comprimento": razao_completa / razao_caracteres,
        "mediana_item": mediana(razoes),
        "min_item": min(razoes),
        "max_item": max(razoes),
        "itens": por_item,
    }


def markdown(relatorio: dict) -> str:
    linhas = [
        "# Benchmark: português brasileiro e inglês, por modelo",
        "",
        "Gerado por `poc/02_benchmark_modelos.py`. Não edite os números à mão.",
        "",
        "Comparação: braço `pt_paralelo` contra braço `en`, nos doze prompts do conjunto v0. Os critérios são os mesmos, as fontes são traduzidas e os dois braços pedem a resposta em português brasileiro. A razão é a soma dos tokens em português dividida pela soma dos tokens em inglês.",
        "",
        "Isto mede quanto o tokenizador da família fragmenta o mesmo pedido. Não mede se o bot responde melhor, alucina menos ou custa menos no fluxo completo. Claude, Gemini e Sabiá aparecem de propósito sem número: o tokenizador não é público e a tabela não os aproxima por outro vocabulário.",
        "",
        f"- Dataset: `{relatorio['dataset_sha256']}`",
        f"- Catálogo: `{relatorio['catalogo_sha256']}`",
        f"- Itens: {relatorio['n_itens']}",
        "- Token especial de início: desligado. A fatura do provedor pode somar um token fixo igual nos dois idiomas; a razão quase não muda, o absoluto sim.",
        "- Envelope de chat (papel `system`, marcadores do produto): fora. Aqui entra o texto do prompt.",
        "",
        "## Razão PT-BR / EN",
        "",
        "Menor razão quer dizer que, neste conjunto, o português ficou mais perto do inglês nesse vocabulário. Não é ranking de qualidade.",
        "",
        "| Modelo | Família | Tokens EN | Tokens PT-BR | PT/EN completo | PT/EN instrução | Mediana por item | Mín. | Máx. | Além do comprimento |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for modelo in relatorio["modelos"]:
        if modelo["status"] != "medido":
            linhas.append(
                f"| {modelo['rotulo']} | {modelo['familia']} | — | — | não medido | — | — | — | — | — |"
            )
            continue
        medicao = modelo["medicao"]
        linhas.append(
            "| {rotulo} | {familia} | {en} | {pt} | {razao} | {inst} | {med} | {mini} | {maxi} | {alem} |".format(
                rotulo=modelo["rotulo"],
                familia=modelo["familia"],
                en=medicao["somas"]["en"]["completo"],
                pt=medicao["somas"]["pt_paralelo"]["completo"],
                razao=fmt(medicao["razao_completo"]),
                inst=fmt(medicao["razao_instrucao"]),
                med=fmt(medicao["mediana_item"]),
                mini=fmt(medicao["min_item"]),
                maxi=fmt(medicao["max_item"]),
                alem=fmt(medicao["alem_do_comprimento"]),
            )
        )

    linhas.extend(
        [
            "",
            "“Além do comprimento” divide a razão de tokens pela razão de caracteres do mesmo par. Perto de 1, a diferença acompanha o tamanho do texto. Acima de 1, o tokenizador fragmenta o português além de ele ser mais longo.",
            "",
            f"Razão de caracteres PT-BR / EN, igual para todos os modelos deste conjunto: {fmt(relatorio['razao_caracteres'])}. Razão de palavras: {fmt(relatorio['razao_palavras'])}.",
            "",
            "## O que ficou de fora, e por quê",
            "",
            "| Modelo | Família | Motivo |",
            "| --- | --- | --- |",
        ]
    )
    for modelo in relatorio["modelos"]:
        if modelo["status"] == "medido":
            continue
        motivo = modelo.get("erro") or modelo.get("nota") or "não medido"
        motivo = motivo.replace("\n", " ")
        linhas.append(f"| {modelo['rotulo']} | {modelo['familia']} | {motivo} |")

    linhas.extend(
        [
            "",
            "## Por tarefa, no vocabulário de referência",
            "",
            "O detalhe por tarefa usa o primeiro modelo medido da família OpenAI com `o200k_base`, quando ele existir. Os outros vocabulários estão no JSON.",
            "",
        ]
    )
    referencia = next(
        (
            modelo
            for modelo in relatorio["modelos"]
            if modelo["status"] == "medido" and modelo["id"] == "gpt-4o"
        ),
        None,
    )
    if referencia is None:
        linhas.append("GPT-4o não foi medido nesta execução. O detalhe por tarefa fica só no JSON dos modelos que rodaram.")
    else:
        linhas.extend(
            [
                f"Referência: {referencia['rotulo']} (`{referencia['ref']}`).",
                "",
                "| Tarefa | Tokens EN | Tokens PT-BR | PT/EN |",
                "| --- | ---: | ---: | ---: |",
            ]
        )
        for item in referencia["medicao"]["itens"]:
            linhas.append(
                f"| {item['id']} | {item['en']['completo']} | {item['pt_paralelo']['completo']} | {fmt(item['razao_completo'])} |"
            )

    linhas.extend(
        [
            "",
            "## Leitura",
            "",
            "- A decisão pré-registrada de H1, H3 e H5 no piloto de um encoding continua em `benchmarks/results/poc_v0_tokenizacao.md`. Esta tabela não reabre esse limiar.",
            "- Não diga que “o português custa X% a mais em todo bot”. A coluna muda de vocabulário para vocabulário, e este n é doze textos escritos para o estudo.",
            "- Não use a linha da Gemma como se fosse o Gemini, nem a do Llama como se fosse o Claude ou o Sabiá.",
            "- Qualidade da resposta por modelo ainda não foi executada. O protocolo está em `docs/benchmark-ptbr-en.md`.",
            "",
        ]
    )
    return "\n".join(linhas) + "\n"


def main() -> int:
    poc = carregar_poc()
    catalogo = json.loads(CATALOGO.read_text(encoding="utf-8"))
    conjunto = json.loads(DATASET.read_text(encoding="utf-8"))
    erros = poc.validar_marcadores(conjunto)
    if erros:
        for erro in erros:
            print(erro, file=sys.stderr)
        return 1

    itens = conjunto["itens"]
    modelos = []
    razao_caracteres = None
    razao_palavras = None
    for modelo in catalogo["modelos"]:
        print(f"medindo {modelo['id']}...", flush=True)
        registro = {
            "id": modelo["id"],
            "rotulo": modelo["rotulo"],
            "familia": modelo["familia"],
            "produto": modelo["produto"],
            "backend": modelo["backend"],
            "ref": modelo.get("ref"),
            "nota": modelo.get("nota", ""),
        }
        try:
            contar = contador_de(modelo)
            medicao = medir_modelo(poc, itens, contar)
        except Exception as exc:
            registro["status"] = "nao-medido"
            registro["erro"] = str(exc)
            modelos.append(registro)
            print(f"  não medido: {exc}", flush=True)
            continue
        registro["status"] = "medido"
        registro["medicao"] = medicao
        modelos.append(registro)
        if razao_caracteres is None:
            razao_caracteres = medicao["razao_caracteres"]
            palavras_pt = medicao["somas"]["pt_paralelo"]["palavras"]
            palavras_en = medicao["somas"]["en"]["palavras"]
            razao_palavras = palavras_pt / palavras_en
        print(
            f"  PT/EN completo {medicao['razao_completo']:.3f}",
            flush=True,
        )

    relatorio = {
        "versao": "v0",
        "n_itens": len(itens),
        "dataset_sha256": poc.sha256_arquivo(DATASET),
        "catalogo_sha256": poc.sha256_arquivo(CATALOGO),
        "comparacao": catalogo["comparacao"],
        "razao_caracteres": razao_caracteres,
        "razao_palavras": razao_palavras,
        "aviso": "Tokenização do par pt_paralelo/en. Sem qualidade e sem preço.",
        "modelos": modelos,
    }
    OUT_JSON.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown(relatorio), encoding="utf-8")
    print(f"escreveu {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
