# Prompts em português brasileiro

Repositório aberto para estudar como escrever prompts em português e quanto isso custa em tokens. O manifesto está em [`MANIFESTO.md`](MANIFESTO.md). As hipóteses, registradas antes da contagem, estão em [`HIPOTESES.md`](HIPOTESES.md).

A tese pública é esta: prompts em português podem ser claros, acessíveis e adequados ao contexto lusófono. O custo de tokenização em relação ao inglês é real e depende do vocabulário. Ele não se resolve com a sigla ABNT, com a retirada de acentos nem com a obrigação de pensar em inglês. Resolve-se, quando se resolve, com instrução menos ambígua e com medição do fluxo inteiro: entrada, saída e retrabalho.

## Benchmark: português brasileiro e inglês, por modelo

A seção compara o mesmo prompt pareado (`pt_paralelo` e `en`) no tokenizador de cada família: GPT-4o, GPT-4, Llama 3.2, Llama 4, Gemma 3, Qwen 3, DeepSeek V3 e Mistral Nemo. Claude, Gemini e Sabiá ficam na tabela sem número enquanto o tokenizador não for público. Isso é custo de leitura do texto, não nota de resposta.

- Protocolo: [`docs/benchmark-ptbr-en.md`](docs/benchmark-ptbr-en.md)
- Tabela gerada: [`benchmarks/results/benchmark_modelos_ptbr_en.md`](benchmarks/results/benchmark_modelos_ptbr_en.md)

## O que este repositório já faz

- Separa norma de citação (ABNT) de estilo de prompt.
- Pré-registra cinco hipóteses e uma rubrica de qualidade ainda não aplicada.
- Conta tokens de doze tarefas pareadas, em inglês, português paralelo, português coloquial, português vago, português otimizado e a mesma versão otimizada sem diacríticos.
- Compara português brasileiro e inglês no tokenizador publicado de várias famílias de modelo.
- Publica o relatório gerado pelo script, com o hash do dataset e o hash das hipóteses.

## O que ainda não faz

- Não chama modelo para gerar resposta.
- Não mede qualidade, alucinação nem reprompt.
- Não converte token em dólar.
- Não inventa a razão de Claude, Gemini ou Sabiá. Sem tokenizador público, a linha fica vazia.

O relatório descritivo, depois da execução local, fica em [`benchmarks/results/poc_v0_tokenizacao.md`](benchmarks/results/poc_v0_tokenizacao.md).

## Mapa

```text
prompt-engineering-ptbr/
├── MANIFESTO.md
├── HIPOTESES.md
├── docs/
│   ├── metodologia.md
│   ├── abnt-escopo.md
│   ├── guia-de-escrita-ptbr.md
│   ├── checklist-de-prompt.md
│   └── referencias.md
├── benchmarks/
│   ├── datasets/
│   ├── results/
│   └── scripts/
├── poc/
│   └── 01_tokenizacao.py
└── evaluation/
    ├── rubricas/
    ├── humanos/
    └── llm-as-judge/
```

## Rodar o piloto

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python poc/01_tokenizacao.py
```

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
