# Benchmark: português brasileiro e inglês, por modelo

Gerado por `poc/02_benchmark_modelos.py`. Não edite os números à mão.

Comparação: braço `pt_paralelo` contra braço `en`, nos doze prompts do conjunto v0. Os critérios são os mesmos, as fontes são traduzidas e os dois braços pedem a resposta em português brasileiro. A razão é a soma dos tokens em português dividida pela soma dos tokens em inglês.

Isto mede quanto o tokenizador da família fragmenta o mesmo pedido. Não mede se o bot responde melhor, alucina menos ou custa menos no fluxo completo. Claude, Gemini e Sabiá aparecem de propósito sem número: o tokenizador não é público e a tabela não os aproxima por outro vocabulário.

- Dataset: `2e0268f9b8be6672af5dec581c5ae603da05162e398d8bdd3019bf8ee4e4d210`
- Catálogo: `1859e64c569c10ace82e57a7c2abe2fc141c261fe7685f2ffcf29ff6a5816229`
- Itens: 12
- Token especial de início: desligado. A fatura do provedor pode somar um token fixo igual nos dois idiomas; a razão quase não muda, o absoluto sim.
- Envelope de chat (papel `system`, marcadores do produto): fora. Aqui entra o texto do prompt.

## Razão PT-BR / EN

Menor razão quer dizer que, neste conjunto, o português ficou mais perto do inglês nesse vocabulário. Não é ranking de qualidade.

| Modelo | Família | Tokens EN | Tokens PT-BR | PT/EN completo | PT/EN instrução | Mediana por item | Mín. | Máx. | Além do comprimento |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| GPT-4o / GPT-4.1 | OpenAI | 896 | 1011 | 1,128 | 1,121 | 1,114 | 1,083 | 1,247 | 1,097 |
| GPT-4 / GPT-3.5 | OpenAI | 905 | 1168 | 1,291 | 1,276 | 1,257 | 1,160 | 1,522 | 1,255 |
| GPT-OSS | OpenAI | 896 | 1011 | 1,128 | 1,121 | 1,114 | 1,083 | 1,247 | 1,097 |
| Llama 3.2 | Meta | 905 | 1167 | 1,290 | 1,274 | 1,257 | 1,160 | 1,522 | 1,253 |
| Llama 4 | Meta | 886 | 1004 | 1,133 | 1,119 | 1,118 | 1,075 | 1,265 | 1,102 |
| Gemma 3 | Google | 960 | 1086 | 1,131 | 1,117 | 1,113 | 1,065 | 1,262 | 1,100 |
| Qwen 3 | Alibaba | 941 | 1194 | 1,269 | 1,275 | 1,245 | 1,144 | 1,479 | 1,233 |
| DeepSeek V3 | DeepSeek | 913 | 1168 | 1,279 | 1,218 | 1,266 | 1,146 | 1,507 | 1,244 |
| Mistral Nemo | Mistral | 947 | 1129 | 1,192 | 1,166 | 1,178 | 1,101 | 1,354 | 1,159 |
| Claude | Anthropic | — | — | não medido | — | — | — | — | — |
| Gemini | Google | — | — | não medido | — | — | — | — | — |
| Sabiá | Maritaca | — | — | não medido | — | — | — | — | — |

“Além do comprimento” divide a razão de tokens pela razão de caracteres do mesmo par. Perto de 1, a diferença acompanha o tamanho do texto. Acima de 1, o tokenizador fragmenta o português além de ele ser mais longo.

Razão de caracteres PT-BR / EN, igual para todos os modelos deste conjunto: 1,029. Razão de palavras: 1,035.

## O que ficou de fora, e por quê

| Modelo | Família | Motivo |
| --- | --- | --- |
| Claude | Anthropic | A Anthropic não publica o tokenizador. A contagem válida é o endpoint count_tokens da API, com o modelo exato. Este piloto não aproxima Claude por tiktoken. |
| Gemini | Google | O bot Gemini não usa, por definição, o tokenizador da Gemma. Sem a API count_tokens do modelo chamado, a razão fica em aberto. |
| Sabiá | Maritaca | Modelo com foco em português. Sem tokenizador público fixado neste piloto, não há número. Não se deduz a razão a partir do Llama. |

## Por tarefa, no vocabulário de referência

O detalhe por tarefa usa o primeiro modelo medido da família OpenAI com `o200k_base`, quando ele existir. Os outros vocabulários estão no JSON.

Referência: GPT-4o / GPT-4.1 (`o200k_base`).

| Tarefa | Tokens EN | Tokens PT-BR | PT/EN |
| --- | ---: | ---: | ---: |
| resumo-chamados | 77 | 96 | 1,247 |
| resumo-ata | 69 | 86 | 1,246 |
| extrair-chamado | 72 | 78 | 1,083 |
| extrair-cobranca | 79 | 86 | 1,089 |
| classificar-avaliacoes | 65 | 73 | 1,123 |
| classificar-incidentes | 93 | 103 | 1,108 |
| codigo-media-movel | 60 | 67 | 1,117 |
| codigo-validar-cpf | 61 | 70 | 1,148 |
| escolher-fornecedor | 96 | 107 | 1,115 |
| verificar-prazo | 71 | 79 | 1,113 |
| qa-abertura | 71 | 77 | 1,085 |
| qa-tarifa | 82 | 89 | 1,085 |

## Leitura

- A decisão pré-registrada de H1, H3 e H5 no piloto de um encoding continua em `benchmarks/results/poc_v0_tokenizacao.md`. Esta tabela não reabre esse limiar.
- Não diga que “o português custa X% a mais em todo bot”. A coluna muda de vocabulário para vocabulário, e este n é doze textos escritos para o estudo.
- Não use a linha da Gemma como se fosse o Gemini, nem a do Llama como se fosse o Claude ou o Sabiá.
- Qualidade da resposta por modelo ainda não foi executada. O protocolo está em `docs/benchmark-ptbr-en.md`.

