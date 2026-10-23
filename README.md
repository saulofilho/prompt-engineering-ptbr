# Prompts em português brasileiro

Repositório aberto para estudar como escrever prompts em português e quanto isso custa em tokens, e um plugin de skills para o agente aplicar esse método. O manifesto está em [`MANIFESTO.md`](MANIFESTO.md). As hipóteses, registradas antes da contagem, estão em [`HIPOTESES.md`](HIPOTESES.md). A entrada do plugin está em [`skills/using-prompt-ptbr/SKILL.md`](skills/using-prompt-ptbr/SKILL.md).

A tese pública é esta: prompts em português podem ser claros, acessíveis e adequados ao contexto lusófono. O custo de tokenização em relação ao inglês é real e depende do vocabulário. Ele não se resolve com a sigla ABNT, com a retirada de acentos nem com a obrigação de pensar em inglês. Resolve-se, quando se resolve, com instrução menos ambígua e com medição do fluxo inteiro: entrada, saída e retrabalho.

## Plugin

Skills para o agente escrever e revisar o pedido sem transformar o piloto em regra. O manifesto de instalação está em [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json) (`prompt-ptbr`, versão 0.1.0). [`AGENTS.md`](AGENTS.md) manda o agente ler a skill de entrada antes de redigir.

No Cursor, abra este repositório: a pasta `.cursor/skills` repete `skills/`, porque o Windows não segue o link simbólico do Linux. Quando o plugin estiver no marketplace, o comando é `/add-plugin prompt-ptbr`. Outros harnesses ainda não têm pacote próprio.

- [Usar o plugin](skills/using-prompt-ptbr/SKILL.md). Escolhe a skill certa antes de redigir e lista o que o agente não pode afirmar.
- [Escrever](skills/writing-precise-ptbr/SKILL.md). Reescreve o pedido em português: imperativo, regras conferíveis, termo estável e frase de ausência.
- [Conferir](skills/checking-prompt/SKILL.md). Marca o checklist e recusa chamar de otimizada a versão que só ficou curta porque apagou critério.
- [ABNT no pedido](skills/scoping-abnt/SKILL.md). Aplica citação, termo e numeração onde a norma regula, e recusa a sigla como técnica de token.
- [Medir](skills/measuring-tokens/SKILL.md). Manda contar no tokenizador do modelo alvo e deixa Claude, Gemini e Sabiá sem número quando não há resposta da API deles.

## Seções

### Posição e método

- [Manifesto](MANIFESTO.md). Tese do projeto: português preciso é legítimo; a ABNT não é técnica de token; o que o repositório afirma e o que recusa.
- [Hipóteses](HIPOTESES.md). H1 a H5 pré-registradas, com limiar, escopo e o que uma contagem de tokens não pode decidir.
- [Metodologia](docs/metodologia.md). Braços pareados, métricas, razão das somas, tokenizadores e ameaças à validade do piloto.
- [Referências](docs/referencias.md). Fontes em formato de referência, com o que cada uma sustenta e o que não sustenta.

### Escrever em português

- [Escrita precisa](docs/escrita-precisa-ptbr.md). Método para quem precisa ser exato: critério conferível, frase de ausência, diacrítico, termo estável, e o que as normas ABNT emprestam ao pedido.
- [Guia curto](docs/guia-de-escrita-ptbr.md). Dez práticas de clareza, cada uma com o status da evidência (piloto, hipótese ou ainda não medido).
- [Checklist](docs/checklist-de-prompt.md). Conferência antes de tratar uma redação como versão otimizada.
- [Escopo da ABNT](docs/abnt-escopo.md). O que NBR 6023, 6028, 10520 e 14724 fazem neste repositório, e por que a sigla não nomeia um estilo de prompt.

### Benchmarks

- [Protocolo PT-BR e inglês](docs/benchmark-ptbr-en.md). Como a comparação entre idiomas é desenhada, modelo a modelo, e o que fica de fora.
- [Tabela por modelo](benchmarks/results/benchmark_modelos_ptbr_en.md). Razão de tokens do português paralelo sobre o inglês, no tokenizador publicado de cada família. Claude, Gemini e Sabiá ficam sem número.
- [Piloto das hipóteses](benchmarks/results/poc_v0_tokenizacao.md). Contagem dos braços no `o200k_base` e no `cl100k_base`: estrutura, prêmio e diacrítico, com a decisão neste conjunto.
- [Custo em dólar](benchmarks/results/custo_usd.md). Entrada dos doze prompts convertida pela tabela de 22 out. 2026. Só há dólar onde existem tokens medidos e preço verificado.
- [Geração e qualidade](benchmarks/results/geracao_qualidade.md). Chamada ao modelo, nota automática, alucinação verificável, reprompt e dólar do fluxo. Nesta execução as linhas estão vazias: não havia chave de API.
- [Razão medida na API](benchmarks/results/benchmark_api_ptbr_en.md). PT/EN só com o `usage` que o provedor devolve. Sem chamada, a linha não é preenchida com outro tokenizador.

### Avaliação

- [Rubrica](evaluation/rubricas/rubrica_v0.md). Nota de 0 a 10 registrada antes das respostas: formato, critério, fidelidade, ausência e idioma. Reprompt fica fora da nota.
- [Checagem automática](evaluation/automatico/checagem_v0.py). Aplica o que dá para verificar sem pessoa: JSON, tamanho, frase exata e número que não está na fonte.
- [Protocolo de juiz automático](evaluation/llm-as-judge/PROTOCOLO.md). Regras para um modelo julgar resposta. Ainda não executado; não substitui amostra humana.
- [Avaliação humana](evaluation/humanos/README.md). Onde as notas cegas entram. Ainda não há notas.

### Dados e execução

- [Pares v0](benchmarks/datasets/pares_v0.json). Doze tarefas pareadas, com os marcadores de critério que os braços otimizado e coloquial precisam conservar.
- [Léxico v0](benchmarks/datasets/lexico_v0.json). Pares ortográficos para ver fragmentação de token. Não recomenda sinônimo mais curto.
- [Catálogo de modelos](benchmarks/datasets/modelos_v0.json). Tokenizador de cada família. Claude, Gemini e Sabiá ficam como vocabulário não publicado.
- [Preços](benchmarks/datasets/precos_v0.json). Tabela datada usada na conversão para dólar. Modelo sem linha fica sem custo.
- [Prova de conceito](poc/README.md). O que cada script faz: contagem, comparação entre idiomas, dólar e chamada de API.
- [Resultados](benchmarks/results/README.md). Quais arquivos cada script grava, e a regra de não editar o número à mão.
- [Scripts seguintes](benchmarks/scripts/README.md). Onde entra fase nova sem copiar a contagem para fora de `poc/`.

## Mapa

```text
prompt-engineering-ptbr/
├── MANIFESTO.md
├── HIPOTESES.md
├── AGENTS.md
├── .cursor-plugin/plugin.json
├── .cursor/skills/
├── skills/
│   ├── using-prompt-ptbr/
│   ├── writing-precise-ptbr/
│   ├── checking-prompt/
│   ├── scoping-abnt/
│   └── measuring-tokens/
├── docs/
│   ├── metodologia.md
│   ├── benchmark-ptbr-en.md
│   ├── abnt-escopo.md
│   ├── escrita-precisa-ptbr.md
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

Leia [`CONTRIBUTING.md`](CONTRIBUTING.md). Hipótese nova não reescreve `HIPOTESES.md` depois que existe resultado: entra em arquivo de versão seguinte. O combinado de convivência está em [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## Licença

Código, scripts e skills sob a licença MIT, em [`LICENSE`](LICENSE). Texto em `docs/`, `MANIFESTO.md` e `HIPOTESES.md` sob CC BY 4.0: pode copiar e adaptar, com crédito e indicação de mudança.

## Como citar

Enquanto não houver release, cite o commit e a data. Para a penalidade de tokenização em geral, cite Petrov et al. (2023), não este piloto. As referências estão em [`docs/referencias.md`](docs/referencias.md).
