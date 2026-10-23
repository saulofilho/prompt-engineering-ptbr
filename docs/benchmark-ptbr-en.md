# Benchmark entre português brasileiro e inglês, por modelo

Esta é a seção de comparação entre idiomas e entre famílias de modelo. A tabela com os números desta execução está em [`benchmarks/results/benchmark_modelos_ptbr_en.md`](../benchmarks/results/benchmark_modelos_ptbr_en.md). Ela é gerada por `poc/02_benchmark_modelos.py`. O catálogo de modelos é `benchmarks/datasets/modelos_v0.json`.

## O que entra na conta

O mesmo pedido, em duas redações pareadas do conjunto v0:

- `en`: inglês, com os critérios e com o pedido de responder em português brasileiro.
- `pt_paralelo`: a tradução próxima dessa instrução, com a fonte em português.

Não se usa o braço coloquial nem o vago aqui. Esses braços medem empacotamento e omissão de critério, não a distância entre idiomas. O braço otimizado também fica de fora desta tabela: ele muda o estilo, e misturar estilo com idioma estraga a leitura.

Para cada família, o script conta instrução e prompt completo no tokenizador publicado daquele modelo. A razão publicada é a soma dos doze prompts, não a média das razões. Mediana, mínimo e máximo por item mostram se uma tarefa puxa o número.

“Além do comprimento” divide a razão de tokens pela razão de caracteres. Separa “o português ficou mais longo” de “o vocabulário quebra mais a palavra portuguesa”.

O token de início de sequência fica desligado. O envelope de chat do produto (system, tags, ferramentas) fica de fora. Os dois afetam o absoluto e quase não mudam uma comparação em que são iguais nos dois idiomas; quando o envelope for diferente por produto, isso precisa de uma versão própria do benchmark, não de um chute.

## Quais modelos

| Família | O que a linha representa |
| --- | --- |
| OpenAI | `o200k_base` (GPT-4o / GPT-4.1) e `cl100k_base` (GPT-4 / GPT-3.5). São os vocabulários do ChatGPT e da API, não “o ChatGPT” como um bot único. |
| Meta | Llama 3.2 e Llama 4, pelo `tokenizer.json` público. A mesma marca pode mudar de razão quando o vocabulário cresce. |
| Google | Gemma 3 pelo tokenizador publicado. Gemini, o bot, é outra linha e não herda o número da Gemma. |
| Alibaba | Qwen 3. |
| DeepSeek | DeepSeek V3. |
| Mistral | Mistral Nemo. |
| Anthropic | Claude. Sem tokenizador público: a linha fica vazia até alguém rodar `count_tokens` no modelo exato. |
| Maritaca | Sabiá. Sem tokenizador fixado neste piloto: a linha fica vazia. Não se copia a razão do Llama. |

Uma família ausente do catálogo não foi “empatada”. Não foi medida. Para incluir outra, acrescente o repositório do `tokenizer.json` ou o nome do encoding e rode o script. Não cole um percentual de outro corpus.

## O que esta seção não é

Não é o prêmio de Petrov et al. (2023) reimpresso: aquele número é do FLORES-200 no `cl100k_base`. O deste arquivo é dos doze prompts daqui. Os dois podem discordar sem que um esteja “errado”; o corpus mudou.

Não aprove a variante que só é mais curta porque apagou regra. Isso é o braço `pt_vago`.

O dólar da entrada, só onde há preço de tabela e tokens medidos, está em [`benchmarks/results/custo_usd.md`](../benchmarks/results/custo_usd.md).

## Qualidade e chamada ao modelo

O script `poc/04_gerar_e_avaliar.py` chama GPT-4o, Claude Haiku 4.5, Gemini 3.8 Flash e Sabiá-4, aplica a checagem automática, faz no máximo um reprompt quando o formato falha e soma o dólar do fluxo. A razão PT/EN desses bots só é gravada se a API devolver o usage. O relatório desta máquina está em [`benchmarks/results/geracao_qualidade.md`](../benchmarks/results/geracao_qualidade.md) e em [`benchmarks/results/benchmark_api_ptbr_en.md`](../benchmarks/results/benchmark_api_ptbr_en.md). Sem chave, as linhas ficam vazias.

A amostra humana da rubrica continua obrigatória antes de tratar a nota automática como qualidade fechada.
