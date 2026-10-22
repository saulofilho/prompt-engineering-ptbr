# Custo em dólar da entrada

Gerado por `poc/03_custo.py`. Preços em `benchmarks/datasets/precos_v0.json`, consultados em 2026-10-22. A conta é tokens ÷ 1.000.000 × preço de entrada. Não inclui saída, cache, lote nem reprompt.

Modelo aberto sem preço de hospedeiro, e bot sem tokens medidos, ficam sem dólar. O preço de um não preenche o outro.

| Modelo | Tokens EN | Tokens PT-BR | USD entrada EN | USD entrada PT-BR | Diferença |
| --- | ---: | ---: | ---: | ---: | ---: |
| GPT-4o (tokens de GPT-4o / GPT-4.1) | 896 | 1011 | 0,002240 | 0,002527 | 0,000287 |
| GPT-4 / GPT-3.5 | — | — | sem dólar | sem dólar | sem preço de tabela verificado para este vocabulário |
| GPT-OSS | — | — | sem dólar | sem dólar | sem preço de tabela verificado para este vocabulário |
| Llama 3.2 | — | — | sem dólar | sem dólar | sem preço de tabela verificado para este vocabulário |
| Llama 4 | — | — | sem dólar | sem dólar | sem preço de tabela verificado para este vocabulário |
| Gemma 3 | — | — | sem dólar | sem dólar | sem preço de tabela verificado para este vocabulário |
| Qwen 3 | — | — | sem dólar | sem dólar | sem preço de tabela verificado para este vocabulário |
| DeepSeek V3 | — | — | sem dólar | sem dólar | sem preço de tabela verificado para este vocabulário |
| Mistral Nemo | — | — | sem dólar | sem dólar | sem preço de tabela verificado para este vocabulário |
| Claude | — | — | sem dólar | sem dólar | sem tokens medidos neste benchmark |
| Gemini | — | — | sem dólar | sem dólar | sem tokens medidos neste benchmark |
| Sabiá | — | — | sem dólar | sem dólar | sem tokens medidos neste benchmark |

A diferença é o que os doze prompts em português acrescentam na entrada, no preço de tabela daquele modelo. Não é o custo do fluxo: falta a resposta.

Sabiá-4, quando houver tokens da API, usa a tabela em real (R$ 5 entrada e R$ 20 saída por milhão) e a taxa aproximada de R$ 5,14 por dólar publicada pela Maritaca. Sem essa contagem, a linha continua vazia.

