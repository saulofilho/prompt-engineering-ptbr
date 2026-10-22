# Prompts em português brasileiro

Repositório aberto para estudar como escrever prompts em português e quanto isso custa em tokens. O manifesto está em [`MANIFESTO.md`](MANIFESTO.md). As hipóteses, registradas antes da contagem, estão em [`HIPOTESES.md`](HIPOTESES.md).

A tese pública é esta: prompts em português podem ser claros, acessíveis e adequados ao contexto lusófono. O custo de tokenização em relação ao inglês é real e depende do vocabulário. Ele não se resolve com a sigla ABNT, com a retirada de acentos nem com a obrigação de pensar em inglês. Resolve-se, quando se resolve, com instrução menos ambígua e com medição do fluxo inteiro: entrada, saída e retrabalho.

## Benchmarks

- Tokens por modelo, português brasileiro contra inglês: protocolo em [`docs/benchmark-ptbr-en.md`](docs/benchmark-ptbr-en.md), tabela em [`benchmarks/results/benchmark_modelos_ptbr_en.md`](benchmarks/results/benchmark_modelos_ptbr_en.md).
- Piloto das hipóteses (estrutura, prêmio e diacrítico): [`benchmarks/results/poc_v0_tokenizacao.md`](benchmarks/results/poc_v0_tokenizacao.md).
- Dólar da entrada, com preço de tabela datado: [`benchmarks/results/custo_usd.md`](benchmarks/results/custo_usd.md).
- Geração, nota automática, alucinação verificável, reprompt e dólar do fluxo: [`benchmarks/results/geracao_qualidade.md`](benchmarks/results/geracao_qualidade.md).
- Razão PT/EN só com a contagem que a API devolver: [`benchmarks/results/benchmark_api_ptbr_en.md`](benchmarks/results/benchmark_api_ptbr_en.md). Claude, Gemini e Sabiá não herdam número de outro tokenizador.

## O que esta execução mediu

- Conta tokens de doze tarefas pareadas, em inglês, português paralelo, português coloquial, português vago, português otimizado e a mesma versão sem diacríticos.
- Compara português brasileiro e inglês no tokenizador publicado de várias famílias.
- Converte a entrada do GPT-4o em dólar. Nos doze prompts, a diferença foi US$ 0,000287 a mais no português, à tabela de US$ 2,50 por milhão de tokens de entrada. Saída ainda não entra nessa conta.
- Tem script para chamar GPT-4o, Claude Haiku 4.5, Gemini 3.8 Flash e Sabiá-4, pontuar formato e alucinação verificável, fazer um reprompt se o formato falhar e somar o dólar do fluxo.

## O que esta execução não mediu

Nesta máquina não havia chave de API. O script de geração rodou e deixou as quatro linhas sem nota e sem razão. Isso é de propósito: Claude, Gemini e Sabiá continuam vazios até a própria API devolver os tokens.

A nota automática também não substitui a amostra humana da rubrica. Com chave, o comando está na seção de rodar o piloto.

## Mapa

```text
prompt-engineering-ptbr/
├── MANIFESTO.md
├── HIPOTESES.md
├── docs/
│   ├── metodologia.md
│   ├── benchmark-ptbr-en.md
│   ├── abnt-escopo.md
│   ├── guia-de-escrita-ptbr.md
│   ├── checklist-de-prompt.md
│   └── referencias.md
├── benchmarks/
│   ├── datasets/
│   ├── results/
│   └── scripts/
├── poc/
│   ├── 01_tokenizacao.py
│   ├── 02_benchmark_modelos.py
│   ├── 03_custo.py
│   └── 04_gerar_e_avaliar.py
└── evaluation/
    ├── automatico/
    ├── rubricas/
    ├── humanos/
    └── llm-as-judge/
```

## Rodar o piloto

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python poc/01_tokenizacao.py
.venv/bin/python poc/02_benchmark_modelos.py
.venv/bin/python poc/03_custo.py
.venv/bin/python poc/04_gerar_e_avaliar.py
```

Se `python3 -m venv` falhar por falta do pacote `python3-venv`, o `uv` cria o ambiente no lugar:

```bash
uv venv .venv
uv pip install -r requirements.txt --python .venv/bin/python
.venv/bin/python poc/01_tokenizacao.py
.venv/bin/python poc/02_benchmark_modelos.py
.venv/bin/python poc/03_custo.py
.venv/bin/python poc/04_gerar_e_avaliar.py
```

`02` baixa só o `tokenizer.json` dos modelos abertos. Não baixa peso. `03` aplica a tabela de preços aos tokens já contados. `04` chama o modelo se existir chave no ambiente (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY` ou `GOOGLE_API_KEY`, `MARITACA_API_KEY` ou `SABIA_API_KEY`). Sem chave, ele grava a linha como não medida e não inventa a razão.

Só a checagem dos marcadores, sem gravar resultado:

```bash
.venv/bin/python poc/01_tokenizacao.py --checar
```

O script recusa o dataset se a variante coloquial ou a otimizada perder um critério, ou se a variante vaga conservar todos. Não edite o markdown de resultado à mão.

## Contribuir

Leia [`CONTRIBUTING.md`](CONTRIBUTING.md). Hipótese nova não reescreve `HIPOTESES.md` depois que existe resultado: entra em arquivo de versão seguinte.

## Licença

Código sob a licença MIT, em [`LICENSE`](LICENSE). Texto em `docs/`, `MANIFESTO.md` e `HIPOTESES.md` sob CC BY 4.0: pode copiar e adaptar, com crédito e indicação de mudança.

## Como citar

Enquanto não houver release, cite o commit e a data. Para a penalidade de tokenização em geral, cite Petrov et al. (2023), não este piloto. As referências estão em [`docs/referencias.md`](docs/referencias.md).
