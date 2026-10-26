# Guia de escrita em português brasileiro

Cada conselho abaixo é prática de clareza. O status diz o que o piloto v0 já pode sustentar. “Não medido” significa que a qualidade da resposta ainda não foi avaliada.

## 1. Escreva a tarefa antes do contexto

Diga o que fazer e só então cole o texto, os dados ou o código. Separe os blocos com rótulo (`Texto:`, `Dados:`, `Contexto:`).

**Status:** desenho do piloto. O script conta instrução e payload em separado justamente porque o bloco grande dilui a instrução.

## 2. Use imperativo direto

“Resuma”, “Extraia”, “Classifique”, “Liste”, “Escreva”. A forma “eu gostaria que você pudesse” acrescenta participantes e cortesia, não critério.

**Status:** H1 testa o custo em tokens desse empacotamento, com os critérios preservados. Não testa se a resposta fica melhor.

## 3. Corte a cortesia que não informa

“Por favor”, “tudo bem”, “se não for pedir demais” e “obrigado” raramente alteram a tarefa. Se um trato de voz for requisito do produto, ele entra como regra (“tom formal”), não como preâmbulo.

**Status:** mesmo recorte da H1. No conjunto v0 a cortesia foi inserida de propósito.

## 4. Repita o critério na forma curta, não o apague

Número de itens, tamanho, idioma da resposta, campos obrigatórios e o que fazer quando o dado não estiver no texto (“responda exatamente: não informado”) pertencem às duas variantes comparáveis.

**Status:** controle do dataset, verificado por marcadores. A variante `pt_vago` existe para mostrar o oposto: fica curta porque perde critério. H2, que perguntaria se isso piora a resposta, não foi executada.

## 5. Peça o idioma da resposta

“Responda em português brasileiro” vale também quando a instrução está em inglês. Sem essa frase, a comparação de custo mistura idioma do pedido e idioma da entrega.

**Status:** controle desenhado para a H4. A H4 em si não foi medida.

## 6. Use lista quando houver várias restrições

Lista curta dispensa frase de transição. Não encha a lista de itens que repetem o mesmo pedido.

**Status:** prática. O piloto não isola “lista” versus “prosa com os mesmos critérios” como fator único; a variante otimizada usa lista e a coloquial usa prosa, junto com a cortesia. Um experimento futuro pode separar os dois fatores.

## 7. Mantenha os diacríticos

Escreva “não”, “ação”, “informação”. A grafia sem acento é outro objeto, mais ambíguo, e não é um modo econômico garantido. Em vocabulários que já contêm a palavra acentuada, a forma sem acento pode até fragmentar mais.

**Status:** H5 testa a diferença de tokens no conjunto v0. A recomendação de manter o acento vale pela língua, mesmo se a contagem oscilar pouco.

## 8. Não troque o termo para “caber” no tokenizador

“Ação” e “atuar” não são intercambiáveis. Um glossário do produto deve fixar o termo certo, não o termo mais barato. Se duas grafias forem sinônimas de verdade no domínio, aí sim a contagem pode desempatar.

**Status:** fora das hipóteses. O léxico do piloto mostra fragmentação; não sugere substituto.

## 9. Não traduza o fluxo inteiro para o inglês por reflexo

Traduzir pode reduzir token de entrada e também pode deslocar exemplo, unidade, praça e obrigação legal. Meça entrada, saída e retrabalho com a resposta no idioma que o usuário lê.

**Status:** H3 cobre a entrada pareada. H4, o fluxo, está em aberto.

## 10. Prefira um exemplo curto a um parágrafo de explicação

Um exemplo do formato de saída, pequeno e fiel, costuma delimitar melhor do que uma segunda explicação da mesma regra. Exemplo inchado custa token e ensina o modelo a imitar o excesso.

**Status:** prática. Não isolada no v0.

As formas prontas por tipo de tarefa estão em `docs/padroes-de-prompt.md`. Quem precisa de precisão extrema, com o lastro de cada dica e o uso correto da ABNT, segue `docs/escrita-precisa-ptbr.md`.

## Ordem sugerida

1. Tarefa, em uma frase no imperativo.
2. Regras verificáveis, em lista.
3. Idioma e formato da resposta.
4. O que fazer se a informação não estiver na fonte.
5. A fonte, num bloco separado.
6. Se ainda houver ambiguidade, um exemplo mínimo.
