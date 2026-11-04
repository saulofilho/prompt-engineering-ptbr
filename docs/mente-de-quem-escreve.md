# O prompt como externalização de contexto tácito

O arquivo continua em `docs/mente-de-quem-escreve.md`. O título nomeia a tese, não um estudo da mente do modelo.

Esta seção formula uma proposição sobre quem escreve o pedido. A dificuldade observável de um prompt está na omissão do que o autor trata como óbvio. Psicologia cognitiva, pragmática e sociologia da linguagem oferecem mecanismos para essa omissão. O repositório não testa esses mecanismos. Deriva deles critérios que um leitor humano pode marcar no texto. Citação de Grice ou de Bell não confirma a H1, a H2 nem a H6.

**Tese central.** A falha observável que esta seção isola não é falta de vocabulário técnico nem falta de cortesia. É contexto tácito que permanece fora do texto. Quem escreve conhece a tarefa, o destinatário, os termos e o critério de aceitação, e nem sempre consegue tratar isso como ausente para quem lê só o prompt. Os padrões do repositório propõem externalizar esse contexto em unidades verificáveis. A tese não afirma que o modelo pensa, sente ou interpreta como pessoa. Afirma que o prompt pode ser lido como registro incompleto de uma assimetria de informação entre autor e sistema.

| Peça | Definição nesta seção |
| --- | --- |
| Construto | Contexto tácito: informação necessária à tarefa que o autor possui e não escreve |
| Mecanismo proposto | Quem escreve subestima a distância entre o que sabe e o que o leitor, humano ou modelo, recupera do texto |
| Intervenção | Externalizar esse contexto em bloco localizável: `Termo:`, `Texto:`, `Público:`, fonte rotulada, frase de ausência |
| Desfecho observável | Presença ou ausência de um critério necessário no prompt |
| O que não é desfecho | Qualidade, inteligência ou eficácia do modelo |

## Definições operacionais

- **Critério necessário.** Informação sem a qual a tarefa não se executa nem se confere conforme a especificação fechada antes da redação.
- **Omissão.** O critério necessário está na lista e não está no prompt. “Ambíguo” não conta como presente.
- **Externalização.** A informação tácita vira declaração localizável no prompt.
- **Unidade de análise.** O prompt produzido por uma pessoa, numa condição.
- **Unidade de observação.** Cada critério da lista fechada.
- **Desfecho primário.** Proporção de critérios necessários omitidos, na soma dos pares pessoa-critério.
- **Desfecho secundário.** Tokens do prompt produzido, só quando a pergunta for o custo de externalizar. Não decide a tese.

“O critério óbvio some” não é medida. A medida é: o autor omitiu o critério X, que já estava na lista.

## Três mecanismos, um desfecho

| Campo | Pergunta sobre quem escreve | Mecanismo proposto | Operacionalização | Status empírico |
| --- | --- | --- | --- | --- |
| Psicologia cognitiva | Por que informação que o autor conhece deixa de aparecer? | Maldição do conhecimento: dificuldade de simular quem não sabe | `Termo:` e a regra que parecia óbvia | Não testado neste repositório |
| Pragmática e filosofia da linguagem | O que a frase torna explícito, implícito ou pressuposto? | Ato de fala, implicatura e terreno comum que não foi estabelecido | Imperativo, `Texto:`, `não informado` | Não testado neste repositório |
| Sociologia da linguagem | Para quem o autor imagina escrever, e qual língua lhe parece legítima? | Audiência imaginada e ideologia linguística | `Público:` e idioma declarado da resposta | Não testado neste repositório |

## Psicologia cognitiva

Camerer, Loewenstein e Weber (1989) definiram a maldição do conhecimento como a incapacidade sistemática de quem está mais informado ignorar a informação privada ao prever o juízo de quem está menos informado. O artigo é de economia experimental. Não é um experimento de prompt. O elo é estrutural: o autor tem uma definição privada e escreve como se ela já estivesse no texto.

Newton (1990), na tese de Stanford, pediu que pessoas batucassem uma melodia conhecida. Quem batucava estimou que metade dos ouvintes reconheceria a música. Os ouvintes reconheceram duas em cento e cinquenta. Recontos posteriores arredondam isso para cerca de 2,5% ou para três acertos em cento e vinte. O número que esta seção usa é o do resumo da tese. Quem conhece a melodia ouve o resto na cabeça. Quem só escuta o dedo na mesa ouve o toque. Quem escreve o prompt está na posição de quem batuca. O modelo recebe a sequência. Isso é analogia de posição, não replicação do experimento.

A omissão, se a tese estiver certa, não é só descuido aleatório. É a dificuldade de tratar como ausente o que para o autor está presente. A medida correspondente é contar critérios de uma lista fechada, não medir carga cognitiva. Sweller (1988) e Norman (1986; 2013) ficam como literatura de desenho da intervenção: carga que não informa a tarefa, fosso entre intenção e instrução, fosso entre resultado e a capacidade de dizer se ele serviu. Nenhum dos dois foi medido no piloto. A H1 contou tokens de cortesia. Araújo (2025) contou resposta de modelo. São colunas diferentes.

O limite “sete mais ou menos dois” não vira regra de prompt. Cowan (2001) reviu a capacidade de curto prazo. Nem sete nem quatro justificam a cota de um resumo. A cota existe porque se confere.

## Pragmática

Um prompt também é um ato dirigido a um sistema. A condição mínima que esta seção exige não é o modelo “compreender” a intenção. É um leitor humano conseguir apontar tarefa, fonte, escopo e o que fazer se o dado não estiver na fonte.

Grice (1975) descreveu a conversa entre pessoas: nem menos nem mais do que a troca pede, com modo claro e com o que se tem base para dizer. O braço vago diz de menos. O braço coloquial e o parágrafo que repete o pedido dizem de mais, sem informação nova. Grice não estudou tokenizador e não decide a H2.

Austin (1962) e Searle (1969) tratam a frase como ato. “Resuma o texto” nomeia o ato e o objeto. “Eu gostaria que você pudesse” esconde o ato. O imperativo torna o pedido inspecionável. Isso não afirma que o modelo reconheça atos de fala.

Clark (1996) chama de terreno comum o que os falantes podem tratar como já sabido. Escritório, glossário interno e a reunião de ontem não são terreno comum com um modelo. O bloco `Texto:` recusa esse apoio. A frase `não informado` cria uma categoria observável para o que a fonte não traz.

## Sociologia da linguagem

A formulação segue uma audiência imaginada e uma crença sobre qual língua e qual registro são legítimos. Essa crença pode omitir o leitor real da entrega, ou trocar o idioma antes de qualquer medida de custo.

Bell (1984) descreve o estilo como resposta a quem se imagina do outro lado. “Se não for pedir demais” acomoda a um colega, não a quem vai ler a resposta. O bloco `Público:` entra quando esse leitor é outra pessoa. “Responda em português brasileiro” nomeia a audiência da entrega, também quando a instrução está em inglês.

Woolard e Schieffelin (1994) revisam a ideologia linguística: o que uma língua é, para que serve e quem pode usá-la com legitimidade. A pressão para pensar o pedido em inglês, antes de medir, é uma crença desse tipo. Petrov et al. (2023) medem token. A ideologia explica uma decisão que pode ocorrer antes da conta. Os dois níveis não se fundem.

## O que fica de fora

Persuasão, reciprocidade, escassez e autoridade são literatura sobre influenciar pessoas. Não são método para conduzir um modelo. Programação neurolinguística, tipo de personalidade e hemisfério cerebral não entram. Blogue, rede social e página de curso que reconta a maldição do conhecimento não substituem Camerer, Loewenstein e Weber (1989) nem Newton (1990).

## Desenho necessário para testar a tese

A literatura torna o mecanismo plausível. Não valida a tese neste domínio. O desenho mínimo está pré-registrado em `HIPOTESES-v2.md` e ainda não tem participante.

Duas condições, a mesma tarefa. Numa, a pessoa escreve o prompt em liberdade. Na outra, escreve com a lista fechada de critérios da tarefa à vista. Avaliadores cegos marcam, para cada critério, presente, ausente ou ambíguo. O desfecho primário é a proporção de critérios necessários ausentes. Uma análise secundária pode contar os tokens do prompt produzido, para ver o custo de externalizar. Essa conta não decide a hipótese. O estudo exige consentimento, a lista fechada antes das redações e regra de exclusão de redação incompleta. As notas, quando existirem, entram em `evaluation/humanos/`. Hoje essa pasta não tem nota.

## Onde isso encontra o resto

- Padrões e o bloco `Termo:`: `docs/padroes-de-prompt.md`
- Checklist: `docs/checklist-de-prompt.md`
- Contagens já decididas, que esta tese não reabre: `HIPOTESES.md` e `HIPOTESES-v1.md`
- Desenho humano ainda sem dado: `HIPOTESES-v2.md`
- Referências: `docs/referencias.md`
