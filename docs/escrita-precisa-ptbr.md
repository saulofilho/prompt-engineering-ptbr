# Escrita precisa em português brasileiro

Seção para quem escreve o pedido em português e não pode deixar margem. Precisão aqui é critério verificável, termo estável e grafia correta. Não é frase mais longa, nem “português culto”, nem a sigla ABNT usada como estilo de prompt.

Cada dica diz de onde vem. “Piloto v0” são os doze pares deste repositório, no `o200k_base`, descritivos. “Araújo (2025)” é o TCC da UFPE. “Petrov et al. (2023)” é o prêmio de tokenização no FLORES-200. Prática sem esse lastro fica marcada como método de clareza, não como resultado.

## Ordem do pedido

1. Tarefa, numa frase no imperativo.
2. Regras numeradas, cada uma conferível.
3. Definição do termo que não pode oscilar.
4. O que fazer se o dado não estiver na fonte, com a frase exata.
5. Idioma e formato da resposta.
6. A fonte, num bloco com rótulo, separada da instrução.
7. Um exemplo mínimo, só se a regra ainda couber em duas leituras.

## Métodos que os estudos sustentam

### Diga o critério, não repita o pedido

Araújo (2025) comparou níveis de especificidade em português brasileiro e em inglês. A estrutura da instrução pesou mais do que a verbosidade, e a melhora não foi linear: alongar o texto não garante resposta melhor. Precisão é acrescentar uma regra que se possa checar. O segundo parágrafo que reformula o primeiro não é precisão.

No piloto v0, a instrução otimizada gastou 22,9% menos tokens que a coloquial, com os mesmos marcadores de critério. A economia veio de cortar cortesia e conectivo, não de apagar exigência. O braço vago é ainda mais curto e deixa de ser preciso: some o critério.

### Use imperativo e guarde o trato de voz para uma regra

“Resuma”, “Extraia”, “Classifique”, “Liste”, “Escreva”. “Eu gostaria que você pudesse” não torna o pedido mais exato. Se o tom for requisito, escreva a regra: “tom formal, sem saudação”.

### Feche a ausência com uma frase exata

Quando a fonte pode não ter o dado, mande a resposta literal. Exemplo: “se o texto não informar, responda exatamente: não informado”. Sem essa frase, o modelo preenche a lacuna. Isso é o controle de alucinação do desenho v0. A qualidade dessa frase ainda não foi medida em modelo neste repositório; o método é o de não deixar a lacuna sem regra.

### Mantenha o diacrítico

Escreva “não”, “ação”, “informação”, “usuário”. No piloto v0, tirar os diacríticos do prompt otimizado aumentou os tokens em 2,5% no `o200k_base`. A grafia errada não comprou economia nesse vocabulário e aumenta ambiguidade (“e” e “é”, “pode” sem acento não distingue “pôde”). Medição de outro corpus, em vocabulários novos, também viu a forma sem acento ficar mais cara, não mais barata (gsantana.dev, 2026). Aquilo é blogue, não este piloto; os dois apontam o mesmo cuidado.

### Não troque o termo para encurtar

“Ação” não é “atuar”. “Configuração” não vira um sinônimo porque o tokenizador parte a palavra. Defina o termo uma vez e use só ele. O léxico deste repositório mostra a fragmentação; não recomenda substituto.

### Fixe o idioma da resposta

“Responda em português brasileiro” entra também quando a instrução está em inglês. Sem isso, a comparação mistura o idioma do pedido com o idioma da entrega. O custo do fluxo inteiro, incluindo resposta e retrabalho, é a hipótese H4 e ainda não foi medido. O que já se mediu é a entrada: no mesmo conjunto, o português paralelo ficou 1,128 vezes o inglês no `o200k_base`, com só 2,9% mais caracteres. Em outros vocabulários do mesmo conjunto a razão vai de cerca de 1,13 a cerca de 1,29. Petrov et al. (2023) acharam cerca de 1,48 no `cl100k_base` sobre o FLORES-200. O número de um corpus não se copia para o outro. Quem precisa de precisão de custo conta no tokenizador do modelo que vai receber o texto. A regra de “quatro caracteres por token” falha aqui: no piloto, o inglês ficou em 4,27 caracteres por token e o português paralelo em 3,89, no `o200k_base`.

### Não encurte o fluxo inteiro traduzindo para o inglês por reflexo

A entrada em inglês pode sair mais barata e a resposta ainda assim sair no idioma errado, ou perder unidade, praça e obrigação que só estão estáveis em português. Meça o fluxo com a resposta no idioma de quem lê.

## Práticas ABNT que servem à precisão

A ABNT não define prompt. As normas abaixo regulam documento acadêmico. O que se aproveita é o hábito de nomear, separar e tornar o caminho conferível. Detalhe do escopo em `docs/abnt-escopo.md`.

| Norma | O que levar para o pedido preciso | O que não vira regra de prompt |
| --- | --- | --- |
| NBR 10520, citações | Separe cópia e paráfrase. “Copie o valor como está no texto” é citação direta. “Interprete” é outra tarefa e precisa dizer o que pode ser concluído. | Não peça “cite em ABNT” sem dizer a obra, o ano e o que fazer se a fonte não estiver no material. |
| NBR 6023, referências | Se o pedido depende de lei, artigo ou dado externo, indique autor, ano e onde o modelo deve achar o trecho. Fato sem fonte não é preciso: é convite a completar. | A norma não reduz token. Uma referência completa pode alongar o pedido de propósito. |
| NBR 6024, numeração progressiva | Numere as regras (1, 2, 3). Quem confere aponta “a regra 2”, em vez de reexplicar o parágrafo. | Numeração não substitui o critério. “1. Seja claro” não se verifica. |
| NBR 6028, resumo | Se a tarefa for resumo, declare extensão, número de frases e se pode haver citação. Um resumo preciso cabe numa especificação curta. | O resumo acadêmico não é o molde de todo prompt. Palavra-chave de trabalho não é campo de extração, salvo se você a pedir. |
| NBR 14724, estrutura de trabalho | Use introdução, desenvolvimento e conclusão só quando o produto for um trabalho com essa estrutura. Diga o que entra em cada parte. | Não imponha esse esqueleto a extração, classificação ou código. |

### Termo, fato e comentário

Escreva as três coisas em blocos diferentes.

- **Termo.** “Neste pedido, ‘prazo’ significa dias corridos, sem pausa.”
- **Fato.** O que está na fonte, no bloco `Texto:`.
- **Comentário.** O que o modelo pode concluir, e o que está proibido concluir.

Citação direta pede reprodução. Citação indireta pede paráfrase marcada como paráfrase. Misturar as duas no mesmo verbo (“explique e copie”) é o ponto em que a resposta inventa.

### Frase que não admite sinônimo

Se a saída tiver de ser uma string, dê a string. “Responda exatamente: não informado.” “Uma escolha, A ou B.” “Campos: cliente, pedido, problema, prazo.” Sinônimo na resposta (“não consta”, “sem dados”) quebra a conferência mesmo quando o sentido parece o mesmo.

## Modelo curto

```text
Extraia os campos numero, credor, vencimento e valor.

Termo:
- vencimento é a data escrita no texto, não uma data calculada

Regras:
1. Um único objeto JSON, sem texto extra.
2. Copie os valores como estão no texto.
3. Se um campo não estiver no texto, use exatamente: não informado.
4. Responda em português brasileiro.

Texto:
...
```

A regra 3 é o caso de ausência. A regra 2 impede paráfrase do valor. O termo impede que “vencimento” vire “data de emissão”.

## O que parece precisão e não é

- Tirar acento para “simplificar”.
- Trocar termo técnico por um mais curto.
- Alongar com voz culta, oração subordinada e preâmbulo.
- Apagar a regra para o prompt ficar menor.
- Chamar de ABNT uma lista sem fonte, quando a tarefa depende de obra ou norma.
- Estimar o custo do português com um percentual único, ou com o tokenizador de outro modelo.

## Onde conferir

- Piloto de tokens: `benchmarks/results/poc_v0_tokenizacao.md`
- Razão por modelo: `benchmarks/results/benchmark_modelos_ptbr_en.md`
- Padrões para copiar: `docs/padroes-de-prompt.md`
- Guia curto: `docs/guia-de-escrita-ptbr.md`
- Checklist: `docs/checklist-de-prompt.md`
- Escopo da ABNT: `docs/abnt-escopo.md`
- Referências: `docs/referencias.md`
