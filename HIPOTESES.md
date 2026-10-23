# Hipóteses pré-registradas

Versão: v0  
Data de registro: 22 de outubro de 2026  
Estado: registrada antes de qualquer execução de modelo e antes da leitura dos resultados de tokenização do piloto.

Não edite limiares, braços ou critérios deste arquivo depois de existir resultado em `benchmarks/results/`. Uma hipótese nova entra em `HIPOTESES-v1.md` (ou versão seguinte), com data própria. O piloto grava o hash deste arquivo junto com os números.

## Recorte

O piloto v0 mede apenas tokens de entrada em textos pareados. Não mede qualidade, alucinação, reprompt nem custo em moeda. H2 e H4 ficam registradas para a fase seguinte e não podem ser dadas como confirmadas a partir da contagem de tokens.

Encoding primário, definido antes da contagem: `o200k_base` (tiktoken). Encoding secundário: `cl100k_base`. Os dois entram no relatório. A decisão de cada hipótese de tokenização usa só o primário.

Agregação primária: razão das somas (soma dos tokens do braço A dividida pela soma dos tokens do braço B), não a média das razões por item. A mediana das razões por item é descritiva.

Os doze itens foram escritos para o experimento. A variante coloquial recebe cortesia e conectivos de propósito, e conserva os mesmos marcadores de critério da variante otimizada. Um efeito neste conjunto mostra o custo desse empacotamento aqui. Não estima a diferença em prompts reais de usuários.

## H1 — Empacotamento

No conjunto v0, a soma dos tokens das instruções `pt_otimizado` é pelo menos 15% menor que a soma dos tokens das instruções `pt_coloquial` no `o200k_base`.

Escopo: só o texto da instrução, sem o payload. Os marcadores de critério permanecem nos dois braços. A economia, se houver, é de cortesia e conectivo, não de exigência removida.

Decisão neste piloto: confirmada no conjunto se a redução for igual ou superior a 15%; não confirmada no conjunto caso contrário. Com n = 12 e texto escrito pelo projeto, os dois desfechos são descritivos. Nenhum dos dois generaliza sozinho.

## H2 — Estrutura e retrabalho

Prompts `pt_otimizado` produzem maior aderência ao formato pedido do que prompts `pt_vago` com o mesmo objetivo, e reduzem reprompts necessários para obter essa aderência.

`pt_vago` existe para esta hipótese. Gastar menos tokens não o torna melhor: ele omite critérios de propósito.

Não testada no v0. Só poderá ser discutida com a rubrica em `evaluation/rubricas/rubrica_v0.md`, repetições e amostra humana.

## H3 — Prêmio de tokenização

Para o conteúdo pareado (`en` frente a `pt_paralelo`), o português brasileiro soma mais tokens do que o inglês no `o200k_base`, no prompt completo.

O relatório decompõe a razão de tokens pela razão de caracteres e pela razão de palavras, para separar “o português ficou mais longo” de “o tokenizador fragmenta mais”. Esta hipótese não afirma uma porcentagem universal. Corpus e vocabulário mudam o prêmio: Petrov et al. (2023) mediram cerca de 1,48 no `cl100k_base` sobre o FLORES-200; outras medições, em outros textos e vocabulários, encontram prêmios menores. Número de um corpus não se copia para outro.

## H4 — Custo do fluxo

Um prompt em inglês pode custar menos tokens na entrada e ainda assim perder no fluxo, se a resposta vier no idioma errado, exigir tradução ou aumentar retrabalho e perda de contexto local.

Controle previsto na fase de qualidade: o braço `en` já pede a resposta em português brasileiro. A comparação justa de custo total é a que fixa o idioma da resposta. Traduzir a instrução para o inglês e aceitar resposta em inglês é outro produto, não o mesmo.

Não testada no v0.

## H5 — Diacríticos

Remover diacríticos de `pt_otimizado` com normalização Unicode NFKD, no prompt completo, não reduz a soma de tokens em 2% ou mais no `o200k_base`.

A forma sem diacrítico é braço experimental. Não é recomendação de escrita. Uma redução igual ou superior a 2% neste piloto recusa H5 no conjunto. Aumento de tokens, ou redução menor que 2%, é compatível com H5 neste conjunto, ainda sem generalização.

## O que o v0 não decide

- Qualidade, alucinação ou preferência humana.
- Preço em dólar. O custo é tokens vezes a tabela vigente do provedor, e a tabela não fica congelada neste arquivo.
- Tokenizador de Claude, Gemini ou Llama. Contagem de API ou o tokenizador publicado do modelo fica para uma versão seguinte.
- Efeito em prompts longos de produção. Se o payload domina a contagem, a economia da instrução pesa pouco no total. O relatório separa instrução, payload e prompt completo por esse motivo.
- Sinônimo mais barato. Trocar termo técnico para reduzir fragmentos não é hipótese deste projeto.
