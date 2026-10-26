---
name: measuring-tokens
description: >-
  Counts tokens for a Brazilian Portuguese prompt with the target model's
  tokenizer and prices only listed models. Use when the user asks for token
  count, PT-BR versus English cost, or dollar cost. Do not estimate Claude,
  Gemini, or Sabiá from another tokenizer.
---

# Medir tokens

Conte no tokenizador do modelo que vai receber o texto. Não reuse o percentual do piloto.

## Estudo deste repositório

Na raiz do repositório:

```bash
python poc/01_tokenizacao.py
python poc/02_benchmark_modelos.py
python poc/03_custo.py
```

`01` decide H1, H3 e H5 no conjunto v0. `02` compara português paralelo e inglês por família. `03` converte em dólar só onde `benchmarks/datasets/precos_v0.json` tem preço e o benchmark tem tokens.

## Texto novo da pessoa

1. Identifique o modelo alvo.
2. OpenAI com vocabulário público: conte com `tiktoken` (`o200k_base` para GPT-4o / GPT-4.1, `cl100k_base` para GPT-4 / GPT-3.5). Diga o encoding.
3. Modelo aberto com `tokenizer.json` publicado: conte esse arquivo, com token especial de início desligado. Não use tiktoken no lugar.
4. Claude, Gemini e Sabiá: só a contagem que a API daquele modelo devolver (`usage` ou `count_tokens`). Sem chave, a linha fica vazia. Não aproxime por Llama, Gemma ou tiktoken.
5. Dólar: tokens ÷ 1.000.000 × preço da tabela, entrada e saída separadas. Modelo sem linha em `precos_v0.json` fica sem dólar.

## O que não dizer

- Não diga que o português custa 13% ou 29% a mais no texto da pessoa. Esses valores são do conjunto v0.
- Não some instrução e payload para obter o total. A fronteira do tokenizador não é aditiva; conte o prompt concatenado.
- Não trate saída, reprompt ou tradução como já incluídos numa conta só de entrada.
