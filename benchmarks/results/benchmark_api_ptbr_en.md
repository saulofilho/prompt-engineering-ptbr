# PT-BR / EN medido na API do provedor

Esta tabela existe para Claude, Gemini e Sabiá, que não publicam tokenizador. O número só aparece se a chamada devolveu `usage` ou contagem de tokens. Sem chamada, a linha continua vazia.

| Modelo | Tokens EN | Tokens PT-BR | PT/EN | Origem |
| --- | ---: | ---: | ---: | --- |
| GPT-4o | — | — | não medido | sem usage da API |
| Claude Haiku 4.5 | — | — | não medido | sem usage da API |
| Gemini 3.8 Flash | 972 | 1098 | 1,130 | countTokens em 2026-11-22, sem geração |
| Sabiá-4 | — | — | não medido | sem usage da API |

No Gemini (`poc/07_contar_tokens_gemini.py`), o `countTokens` não gera resposta. A documentação não diz se o número é exato nem se inclui envelope de mensagem. O número vale só para este modelo e não se transfere para a Gemma nem para outro Gemini.

Contagem de API não é diretamente comparável à dos tokenizadores locais, que contam o texto sem envelope.

