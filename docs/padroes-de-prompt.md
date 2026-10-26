# Padrões de prompt

Formas para copiar quando o pedido é em português brasileiro. Cada padrão é a forma do braço `pt_otimizado` de um tipo de tarefa dos doze pares em `benchmarks/datasets/pares_v0.json`. A cortesia saiu. O critério ficou.

O que isso sustenta, e de onde:

- Araújo (2025) comparou especificidade em português brasileiro e em inglês. A estrutura pesou mais do que a verbosidade, e alongar o texto não melhorou de forma linear. Estes padrões acrescentam regra conferível, não um segundo parágrafo que repete o primeiro.
- No piloto v0, no `o200k_base`, a instrução otimizada gastou 22,9% menos tokens que a coloquial, com os mesmos marcadores de critério. A diferença é cortesia e conectivo. Vale para este conjunto, escrito para o experimento. Não é lei de prompt de produção.
- A qualidade da resposta, a alucinação e o reprompt destes padrões não foram medidos. Isso é a hipótese H2, ainda aberta. Usar o padrão não autoriza nota de qualidade.

Quem precisa do método completo e da ABNT no lugar certo segue `docs/escrita-precisa-ptbr.md`. A lista de conferência está em `docs/checklist-de-prompt.md`.

## Esqueleto

Todos os braços otimizados do piloto cabem nesta ordem.

```text
[Verbo no imperativo] [objeto da tarefa].

Termo:
- [nome] significa [definição única]

Regras:
- [critério que se confere]
- [formato da resposta]
- se o dado não estiver na fonte, responda exatamente: não informado
- resposta em português brasileiro

Texto:
[fonte]
```

O bloco `Termo:` entra quando a palavra pode oscilar. A frase `não informado` entra quando a fonte pode não ter o dado. O rótulo da fonte no piloto é `Texto:` ou `Contexto:`.

## Resumo com cota

Use quando o produto é um resumo e o tamanho tem de ser conferido.

No piloto: `resumo-chamados`, `resumo-ata`.

```text
Resuma o texto em [N] [tópicos ou frases].

Regras:
- [uma frase por tópico, se for tópico]
- no máximo [N] palavras [por tópico ou por frase]
- resposta em português brasileiro

Texto:
...
```

A cota é o critério. “Resuma bem” não se confere. A NBR 6028 empresta o hábito de declarar extensão; o molde acadêmico de resumo não entra se a tarefa não for um resumo.

## Extração de campos

Use quando a saída é um objeto com campos nomeados.

No piloto: `extrair-chamado`, `extrair-cobranca`.

```text
Extraia os campos [campo], [campo] e [campo].

Regras:
- um único objeto JSON
- sem texto extra
- copie os valores como estão no texto
- se um campo não estiver no texto, use exatamente: não informado
- valores em português brasileiro

Texto:
...
```

“Copie os valores como estão no texto” impede paráfrase do número, da data e do nome. Sem a frase de ausência, o campo vazio vira convite a completar.

## Classificação com rótulo fechado

Use quando cada item recebe uma classe de uma lista fechada.

No piloto: `classificar-avaliacoes`.

```text
Classifique cada item como [rótulo], [rótulo] ou [rótulo].

Regras:
- array JSON com [N] objetos
- campos [id] e [classe]
- sem texto extra

Texto:
...
```

O rótulo permitido está escrito. “O que você acha” é o braço vago deste tipo: some a lista e o formato.

## Classificação com definição

Use quando o rótulo só é estável se a definição vier no pedido.

No piloto: `classificar-incidentes`.

```text
Classifique cada frase como [P1], [P2] ou [P3].

Definições:
- [P1]: [o que conta como este rótulo]
- [P2]: [o que conta como este rótulo]
- [P3]: [o que conta como este rótulo]

Regras:
- array JSON de objetos com os campos [id] e [prioridade]
- sem texto extra

Texto:
...
```

A definição é o termo estável. Trocar “indisponível para muitos clientes” por um sinônimo mais curto muda a classe, não só o token.

## Código com contrato

Use quando a entrega é código e a assinatura já está decidida.

No piloto: `codigo-media-movel`, `codigo-validar-cpf`.

```text
Escreva a função [linguagem] [nome]([argumentos]) -> [retorno].

Regras:
- [restrição conferível: janela, formato rejeitado, número de testes]
- devolva somente o código
- não explique

Contexto:
...
```

“Somente o código” é critério de formato. A explicação em volta, se for necessária, é outro pedido.

## Escolha fechada

Use quando há alternativas nomeadas e a justificativa tem tamanho máximo.

No piloto: `escolher-fornecedor`.

```text
Escolha [o que].

Regras:
- uma escolha, [A] ou [B]
- justifique em no máximo [N] linhas
- use apenas os dados do texto
- resposta em português brasileiro

Texto:
...
```

“Qual é melhor?” admite critério que não está na fonte. A lista fecha a escolha e o tamanho da justificativa.

## Pergunta com frase de ausência

Use quando a resposta é um fato da fonte e o fato pode não estar lá.

No piloto: `verificar-prazo`, `qa-abertura`, `qa-tarifa`.

```text
Com base apenas no texto, [pergunte o fato].

Regras:
- se o texto não informar, responda exatamente: não informado
- uma frase
- resposta em português brasileiro

Texto:
...
```

A string `não informado` é a que a checagem procura. “Não consta” e “sem dados” quebram a conferência. Quando a resposta válida também é uma string fechada, escreva as duas: `no prazo` ou `fora do prazo`.

## Formas que o piloto separa deste padrão

| Forma | O que é no conjunto v0 | O que a contagem diz |
| --- | --- | --- |
| Coloquial | O mesmo critério, com saudação, pedido e agradecimento | H1: a instrução otimizada ficou 22,9% menor no `o200k_base` |
| Vago | A tarefa sem cota, campo, rótulo ou frase de ausência | Mais curta porque o critério saiu. H2, sobre a resposta, não foi medida |
| Sem diacrítico | O otimizado com acento removido por NFKD | H5: os tokens subiram 2,5% no `o200k_base`. Não é recomendação |
| Instrução em inglês | O braço `en`, com a resposta pedida em português brasileiro | H3: o prompt completo em português paralelo ficou 1,128 vezes o inglês neste conjunto e neste vocabulário. O fluxo inteiro é a H4 e não foi medido |

Petrov et al. (2023) mediram cerca de 1,48 no `cl100k_base` sobre o FLORES-200. Esse número é de outro corpus. Não substitui a contagem do modelo que vai receber o texto.

## Antes de chamar a redação de otimizada

1. O padrão correspondente está preenchido com número, campo, rótulo ou frase exata.
2. O critério do pedido original continua na lista.
3. O checklist em `docs/checklist-de-prompt.md` passa.

Aí a redação está na forma do braço otimizado. A nota da resposta continua por medir.
