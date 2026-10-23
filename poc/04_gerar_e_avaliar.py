#!/usr/bin/env python3
"""Gera respostas, mede formato, alucinação verificável, reprompt e dólar.

Claude, Gemini e Sabiá só entram na razão PT/EN se a API devolver a
contagem de entrada. Não há fallback para tiktoken.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "benchmarks" / "datasets" / "pares_v0.json"
PRECOS = ROOT / "benchmarks" / "datasets" / "precos_v0.json"
OUT_JSON = ROOT / "benchmarks" / "results" / "geracao_qualidade.json"
OUT_MD = ROOT / "benchmarks" / "results" / "geracao_qualidade.md"
OUT_API = ROOT / "benchmarks" / "results" / "benchmark_api_ptbr_en.md"

BRACOS = ("en", "pt_paralelo", "pt_coloquial", "pt_otimizado", "pt_vago")
REPROMPT = (
    "A resposta anterior não cumpriu o formato pedido. "
    "Envie somente a resposta refeita, obedecendo às regras do pedido original."
)
PROVEDORES = [
    {
        "id": "gpt-4o",
        "rotulo": "GPT-4o",
        "tipo": "openai",
        "model": "gpt-4o",
        "env": ["OPENAI_API_KEY"],
        "preco_id": "gpt-4o",
        "url": "https://api.openai.com/v1/chat/completions",
    },
    {
        "id": "claude",
        "rotulo": "Claude Haiku 4.5",
        "tipo": "anthropic",
        "model": "claude-haiku-4-5",
        "env": ["ANTHROPIC_API_KEY"],
        "preco_id": "claude-haiku-4-5",
        "url": "https://api.anthropic.com/v1/messages",
    },
    {
        "id": "gemini",
        "rotulo": "Gemini 3.8 Flash",
        "tipo": "gemini",
        "model": "gemini-3.8-flash",
        "env": ["GEMINI_API_KEY", "GOOGLE_API_KEY"],
        "preco_id": "gemini-3.8-flash",
    },
    {
        "id": "sabia",
        "rotulo": "Sabiá-4",
        "tipo": "openai",
        "model": "sabia-4",
        "env": ["MARITACA_API_KEY", "SABIA_API_KEY"],
        "preco_id": "sabia-4",
        "url": "https://chat.maritaca.ai/api/chat/completions",
    },
]


def carregar(caminho: Path, nome: str):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"não foi possível carregar {caminho}")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def chave(nomes: list[str]) -> str | None:
    for nome in nomes:
        valor = os.environ.get(nome)
        if valor:
            return valor
    return None


def post(url: str, payload: dict, headers: dict) -> dict:
    pedido = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(pedido, timeout=90) as resposta:
            return json.loads(resposta.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        corpo = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"HTTP {exc.code}: {corpo}") from exc


def chamar(provedor: dict, messages: list[dict], segredo: str) -> tuple[str, int | None, int | None]:
    tipo = provedor["tipo"]
    if tipo == "openai":
        dados = post(
            provedor["url"],
            {"model": provedor["model"], "temperature": 0, "messages": messages},
            {"Authorization": f"Bearer {segredo}", "Content-Type": "application/json"},
        )
        texto = dados["choices"][0]["message"]["content"]
        uso = dados.get("usage") or {}
        return texto, uso.get("prompt_tokens"), uso.get("completion_tokens")
    if tipo == "anthropic":
        dados = post(
            provedor["url"],
            {
                "model": provedor["model"],
                "max_tokens": 600,
                "temperature": 0,
                "messages": messages,
            },
            {
                "x-api-key": segredo,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
        )
        texto = dados["content"][0]["text"]
        uso = dados.get("usage") or {}
        return texto, uso.get("input_tokens"), uso.get("output_tokens")
    if tipo == "gemini":
        conteudos = []
        for mensagem in messages:
            papel = "model" if mensagem["role"] == "assistant" else "user"
            conteudos.append({"role": papel, "parts": [{"text": mensagem["content"]}]})
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{provedor['model']}:generateContent?key={segredo}"
        )
        dados = post(
            url,
            {"contents": conteudos, "generationConfig": {"temperature": 0}},
            {"Content-Type": "application/json"},
        )
        texto = dados["candidates"][0]["content"]["parts"][0]["text"]
        uso = dados.get("usageMetadata") or {}
        return texto, uso.get("promptTokenCount"), uso.get("candidatesTokenCount")
    raise RuntimeError(f"provedor desconhecido: {tipo}")


def prompt_de(poc, item: dict, braco: str) -> str:
    if braco == "en":
        return poc.montar_completo(item["instrucao"][braco], item["rotulo_en"], item["fonte_en"])
    return poc.montar_completo(item["instrucao"][braco], item["rotulo_pt"], item["fonte_pt"])


def usd_de(tokens: int | None, por_milhao: float | None) -> float | None:
    if tokens is None or por_milhao is None:
        return None
    return tokens / 1_000_000 * por_milhao


def preco_do(tabela: dict, preco_id: str, cambio: float) -> dict:
    item = tabela[preco_id]
    if "entrada_usd_por_milhao" in item:
        return {
            "entrada": item["entrada_usd_por_milhao"],
            "saida": item["saida_usd_por_milhao"],
            "moeda": "USD",
        }
    return {
        "entrada": item["entrada_brl_por_milhao"] / cambio,
        "saida": item["saida_brl_por_milhao"] / cambio,
        "entrada_brl": item["entrada_brl_por_milhao"],
        "saida_brl": item["saida_brl_por_milhao"],
        "moeda": "BRL",
    }


def fmt(valor: float | None) -> str:
    if valor is None:
        return "—"
    return f"{valor:.6f}".replace(".", ",")


def executar(provedor, segredo, poc, itens, checar, repeticoes: int) -> dict:
    chamadas = []
    for item in itens:
        for braco in BRACOS:
            for repeticao in range(repeticoes):
                mensagens = [{"role": "user", "content": prompt_de(poc, item, braco)}]
                texto, entrada, saida = chamar(provedor, mensagens, segredo)
                avaliacao = checar(item["id"], texto, braco)
                reprompts = 0
                entrada_total = entrada
                saida_total = saida
                if not avaliacao["formato_util"]:
                    mensagens.append({"role": "assistant", "content": texto})
                    mensagens.append({"role": "user", "content": REPROMPT})
                    texto2, entrada2, saida2 = chamar(provedor, mensagens, segredo)
                    reprompts = 1
                    avaliacao = checar(item["id"], texto2, braco)
                    texto = texto2
                    if None in (entrada_total, entrada2, saida_total, saida2):
                        entrada_total = None
                        saida_total = None
                    else:
                        entrada_total += entrada2
                        saida_total += saida2
                chamadas.append(
                    {
                        "id": item["id"],
                        "braco": braco,
                        "repeticao": repeticao,
                        "reprompts": reprompts,
                        "entrada": entrada,
                        "saida": saida,
                        "entrada_fluxo": entrada_total,
                        "saida_fluxo": saida_total,
                        "avaliacao": avaliacao,
                        "resposta": texto,
                    }
                )
                print(f"  {item['id']} {braco} reprompt={reprompts}", flush=True)
    return {"chamadas": chamadas}


def resumir(bloco: dict, preco: dict) -> dict:
    chamadas = bloco["chamadas"]
    def soma(campo):
        valores = [chamada[campo] for chamada in chamadas]
        if any(valor is None for valor in valores):
            return None
        return sum(valores)

    entrada = soma("entrada_fluxo")
    saida = soma("saida_fluxo")
    def tokens_braco(braco: str) -> int | None:
        valores = [
            chamada["entrada"]
            for chamada in chamadas
            if chamada["braco"] == braco and chamada["repeticao"] == 0 and chamada["reprompts"] >= 0
        ]
        # entrada da primeira chamada está em "entrada", mesmo se houve reprompt
        if any(valor is None for valor in valores) or not valores:
            return None
        return sum(valores)

    en = tokens_braco("en")
    pt = tokens_braco("pt_paralelo")
    razao = None if en in (None, 0) or pt is None else pt / en
    alucinacoes = sum(1 for chamada in chamadas if chamada["avaliacao"]["alucinacao"])
    reprompts = sum(chamada["reprompts"] for chamada in chamadas)
    notas = [chamada["avaliacao"]["nota"] for chamada in chamadas if chamada["avaliacao"]["nota"] is not None]
    return {
        "chamadas": len(chamadas),
        "reprompts": reprompts,
        "alucinacoes": alucinacoes,
        "nota_media": (sum(notas) / len(notas)) if notas else None,
        "entrada": entrada,
        "saida": saida,
        "usd": None
        if entrada is None or saida is None
        else usd_de(entrada, preco["entrada"]) + usd_de(saida, preco["saida"]),
        "razao_pt_en": razao,
        "tokens_en": en,
        "tokens_pt": pt,
        "razao_origem": "usage da API na primeira chamada, sem reprompt",
    }


def markdown(relatorio: dict) -> str:
    linhas = [
        "# Geração, qualidade, alucinação e reprompt",
        "",
        "Gerado por `poc/04_gerar_e_avaliar.py`. A nota é a checagem automática da rubrica v0. Não há amostra humana nesta execução, então a nota não fecha a rubrica sozinha.",
        "",
        "Alucinação aqui é contradição com o gabarito verificável ou número que não está na fonte. Reprompt é uma segunda chamada, só quando o formato não ficou utilizável, e entra no dólar do fluxo, fora da nota.",
        "",
        f"- Repetições pedidas: {relatorio['repeticoes']}",
        "- Temperatura: 0",
        "- Braços: en, pt_paralelo, pt_coloquial, pt_otimizado, pt_vago",
        "",
        "| Modelo | Chamadas | Reprompts | Alucinações | Nota média | Tokens entrada | Tokens saída | USD do fluxo | PT/EN na API |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for modelo in relatorio["modelos"]:
        if modelo["status"] != "medido":
            linhas.append(
                f"| {modelo['rotulo']} | — | — | — | — | — | — | — | não medido |"
            )
            continue
        resumo = modelo["resumo"]
        nota = "—" if resumo["nota_media"] is None else f"{resumo['nota_media']:.2f}".replace(".", ",")
        razao = "—" if resumo["razao_pt_en"] is None else f"{resumo['razao_pt_en']:.3f}".replace(".", ",")
        linhas.append(
            "| {rotulo} | {n} | {rep} | {alu} | {nota} | {ent} | {sai} | {usd} | {razao} |".format(
                rotulo=modelo["rotulo"],
                n=resumo["chamadas"],
                rep=resumo["reprompts"],
                alu=resumo["alucinacoes"],
                nota=nota,
                ent=resumo["entrada"] if resumo["entrada"] is not None else "—",
                sai=resumo["saida"] if resumo["saida"] is not None else "—",
                usd=fmt(resumo["usd"]),
                razao=razao,
            )
        )
    linhas.extend(["", "## Provedores sem chamada", "", "| Modelo | Motivo |", "| --- | --- |"])
    for modelo in relatorio["modelos"]:
        if modelo["status"] == "medido":
            continue
        linhas.append(f"| {modelo['rotulo']} | {modelo.get('erro', 'não medido')} |")
    linhas.extend(
        [
            "",
            "A coluna PT/EN usa apenas os tokens de entrada que a própria API devolveu, no braço inglês e no português paralelo, na primeira chamada. Se esse campo não veio, a razão fica vazia. Ela não é copiada do tiktoken nem de outro bot.",
            "",
        ]
    )
    return "\n".join(linhas) + "\n"


def markdown_api(relatorio: dict) -> str:
    linhas = [
        "# PT-BR / EN medido na API do provedor",
        "",
        "Esta tabela existe para Claude, Gemini e Sabiá, que não publicam tokenizador. O número só aparece se a chamada devolveu `usage`. Sem chamada, a linha continua vazia.",
        "",
        "| Modelo | Tokens EN | Tokens PT-BR | PT/EN | Origem |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for modelo in relatorio["modelos"]:
        if modelo["status"] != "medido" or modelo["resumo"]["razao_pt_en"] is None:
            linhas.append(f"| {modelo['rotulo']} | — | — | não medido | sem usage da API |")
            continue
        resumo = modelo["resumo"]
        linhas.append(
            f"| {modelo['rotulo']} | {resumo['tokens_en']} | {resumo['tokens_pt']} | "
            f"{resumo['razao_pt_en']:.3f}".replace(".", ",")
            + f" | {resumo['razao_origem']} |"
        )
    linhas.append("")
    return "\n".join(linhas) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeticoes", type=int, default=1)
    args = parser.parse_args()
    poc = carregar(ROOT / "poc" / "01_tokenizacao.py", "poc_tokenizacao")
    checagem = carregar(ROOT / "evaluation" / "automatico" / "checagem_v0.py", "checagem_v0")
    conjunto = json.loads(DATASET.read_text(encoding="utf-8"))
    precos = json.loads(PRECOS.read_text(encoding="utf-8"))
    tabela = {item["id"]: item for item in precos["modelos"]}
    cambio = precos["cambio_brl_por_usd"]["valor"]
    modelos = []
    for provedor in PROVEDORES:
        segredo = chave(provedor["env"])
        if not segredo:
            modelos.append(
                {
                    "id": provedor["id"],
                    "rotulo": provedor["rotulo"],
                    "status": "nao-medido",
                    "erro": "sem chave de API neste ambiente; a razão não foi inventada",
                }
            )
            print(f"{provedor['id']}: sem chave", flush=True)
            continue
        print(f"gerando {provedor['id']}...", flush=True)
        try:
            bloco = executar(
                provedor,
                segredo,
                poc,
                conjunto["itens"],
                checagem.avaliar,
                args.repeticoes,
            )
            resumo = resumir(bloco, preco_do(tabela, provedor["preco_id"], cambio))
        except Exception as exc:
            modelos.append(
                {
                    "id": provedor["id"],
                    "rotulo": provedor["rotulo"],
                    "status": "nao-medido",
                    "erro": str(exc),
                }
            )
            print(f"  falhou: {exc}", flush=True)
            continue
        modelos.append(
            {
                "id": provedor["id"],
                "rotulo": provedor["rotulo"],
                "model": provedor["model"],
                "status": "medido",
                "resumo": resumo,
                "chamadas": bloco["chamadas"],
            }
        )
    relatorio = {
        "repeticoes": args.repeticoes,
        "aviso": "Checagem automática. Sem amostra humana. Sem razão inventada.",
        "modelos": modelos,
    }
    OUT_JSON.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown(relatorio), encoding="utf-8")
    OUT_API.write_text(markdown_api(relatorio), encoding="utf-8")
    print(f"escreveu {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
