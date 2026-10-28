# Forma controlada, v1

Gerado por `poc/05_controlado.py`. Não edite os números à mão.

Dataset controlado: `35c7b6a4496afe075bb258aa6a61b6fd83853470b15b880ca862db973831b236`
Hipóteses v1: `c1c41f49c02515d1e8d7bc2376cc4287cbf4fce62ebd24bccffca9dcec6ea525`

H6 compara a soma da instrução `pt_controlado` com a soma da instrução `pt_otimizado`. Redução de 15% ou mais recusa H6 neste conjunto. O prompt completo não decide.

Decisão no `o200k_base`: compatível com H6 neste conjunto.

| Escopo | Tokens otimizado | Tokens controlado | Razão | Redução |
| --- | ---: | ---: | ---: | ---: |
| Instrução | 487 | 514 | 1,055 | -5,5% |
| Completo | 1020 | 1035 | 1,015 | -1,5% |

Razão acima de 1: a forma controlada gastou mais tokens do que a otimizada. Redução negativa é aumento.

## Por item, instrução, o200k_base

| Item | Otimizado | Controlado |
| --- | ---: | ---: |
| resumo-chamados | 31 | 37 |
| resumo-ata | 26 | 28 |
| extrair-chamado | 31 | 35 |
| extrair-cobranca | 36 | 37 |
| classificar-avaliacoes | 32 | 38 |
| classificar-incidentes | 64 | 66 |
| codigo-media-movel | 45 | 45 |
| codigo-validar-cpf | 51 | 48 |
| escolher-fornecedor | 39 | 40 |
| verificar-prazo | 42 | 45 |
| qa-abertura | 44 | 47 |
| qa-tarifa | 46 | 48 |

No `cl100k_base`, a instrução controlada soma 590 tokens e a otimizada soma 578 (razão 1,021). Esse encoding não decide H6.

## H7

Os estímulos estão em `benchmarks/datasets/formatos_v1.json`. A saída não foi medida. Sem o `usage` da API, esta seção não recebe número.
