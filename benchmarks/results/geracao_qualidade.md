# Geração, qualidade, alucinação e reprompt

Gerado por `poc/04_gerar_e_avaliar.py`. A nota é a checagem automática da rubrica v0. Não há amostra humana nesta execução, então a nota não fecha a rubrica sozinha.

Alucinação aqui é contradição com o gabarito verificável ou número que não está na fonte. Reprompt é uma segunda chamada, só quando o formato não ficou utilizável, e entra no dólar do fluxo, fora da nota.

- Repetições pedidas: 1
- Temperatura: 0
- Braços: en, pt_paralelo, pt_coloquial, pt_otimizado, pt_vago

| Modelo | Chamadas | Reprompts | Alucinações | Nota média | Tokens entrada | Tokens saída | USD do fluxo | PT/EN na API |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| GPT-4o | — | — | — | — | — | — | — | não medido |
| Claude Haiku 4.5 | — | — | — | — | — | — | — | não medido |
| Gemini 3.8 Flash | — | — | — | — | — | — | — | não medido |
| Sabiá-4 | — | — | — | — | — | — | — | não medido |

## Provedores sem chamada

| Modelo | Motivo |
| --- | --- |
| GPT-4o | sem chave de API neste ambiente; a razão não foi inventada |
| Claude Haiku 4.5 | sem chave de API neste ambiente; a razão não foi inventada |
| Gemini 3.8 Flash | sem chave de API neste ambiente; a razão não foi inventada |
| Sabiá-4 | sem chave de API neste ambiente; a razão não foi inventada |

A coluna PT/EN usa apenas os tokens de entrada que a própria API devolveu, no braço inglês e no português paralelo, na primeira chamada. Se esse campo não veio, a razão fica vazia. Ela não é copiada do tiktoken nem de outro bot.

