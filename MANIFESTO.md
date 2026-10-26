# Manifesto por prompts em português que se medem

## Resumo

Este projeto trata de como escrever prompts em português brasileiro e de quanto isso custa em tokens, com registro aberto do que já se sabe e do que ainda é hipótese. A literatura mostra que o mesmo conteúdo em português tende a ocupar mais tokens do que em inglês, e que a diferença muda conforme o tokenizador e o corpus. Isso não autoriza concluir que escrever em inglês seja sempre mais barato no fluxo completo, nem que a norma da ABNT seja um método de compressão. A ABNT, neste repositório, regula citações e referências do próprio estudo. O manual de escrita recomenda português técnico claro: verbo no imperativo, critérios explícitos, listas e preservação dos diacríticos. Essas recomendações visam reduzir ambiguidade. O efeito delas sobre tokens e sobre a qualidade da resposta é objeto de hipóteses pré-registradas. A prova de conceito inicial apenas conta tokens de doze tarefas pareadas, em variantes controladas, e não avalia respostas de modelos. O repositório existe para que a comunidade lusófona acumule evidência reprodutível, em vez de repetir atalhos sem medição.

**Palavras-chave:** Engenharia de prompt. Português brasileiro. Tokenização. Custo de inferência. Método experimental.

## Posição

Prompts em português podem ser eficientes, acessíveis e adequados ao contexto de quem os escreve. O objetivo não é negar o custo de tokenização do português brasileiro. É produzir evidência e práticas que reduzam ambiguidade, retrabalho e desperdício, sem obrigar pessoas lusófonas a pensar em inglês para serem levadas a sério.

A frase que este projeto recusa como tese é: “português correto, no padrão ABNT, economiza tokens”. A frase que ele sustenta é: clareza, critério explícito e medição do fluxo inteiro valem mais do que o idioma escolhido por hábito ou por atalho.

## Princípios

1. **Medir antes de recomendar.** Prática de escrita pode ser ensinada como clareza. Efeito em tokens ou em qualidade só entra como resultado depois de contagem reprodutível.
2. **O português é uma escolha legítima.** Produto, documento e usuário brasileiros não precisam ser traduzidos para o inglês para existirem. A escolha de idioma é de qualidade e de contexto, não só de fatura.
3. **Clareza não é grafia mutilada.** Remover acento, ceder termo técnico a um sinônimo “mais barato” ou imitar telegrama não é otimização. É outro texto.
4. **O custo que importa é o do fluxo.** Entrada, saída, reprompt, tradução e perda de contexto local entram na conta. Um prompt mais curto que gera a resposta errada não economizou.
5. **A norma acadêmica documenta o estudo.** ABNT NBR 6023 e ABNT NBR 10520 organizam referências e citações deste repositório. Não definem um dialeto de prompt.
6. **Resultado nulo também se publica.** Hipótese que não se confirma no conjunto continua no repositório, com o hash do texto que a registrou.

## O que já dá para afirmar, e de onde vem

O prêmio de tokenização existe e não é um detalhe. Petrov et al. (2023), no FLORES-200, encontram o português a cerca de 1,48 vezes os tokens do inglês no tokenizador `cl100k_base` (ChatGPT e GPT-4 da época do artigo). O mesmo artigo não atribui ao Llama um prêmio de 42%. Vocabulários mais novos e outros corpora mudam a razão: por isso este repositório mede o próprio conjunto em vez de herdar um percentual.

Araújo (2025), em trabalho de conclusão de curso na UFPE, comparou especificidade do prompt e idioma (português brasileiro e inglês) em quatro modelos, com 1.500 pares de respostas. A estrutura da instrução pesou mais do que a verbosidade, a melhora não foi linear, e o inglês levou vantagem na avaliação usada — com a ressalva, registrada pela própria autora, de baixa concordância humana e de viés dos juízes automáticos. É evidência a considerar, não um veredito universal, e o gênero é TCC, não artigo de periódico.

Medições de blogue e de repositório ilustram o mecanismo e não substituem o piloto daqui. Servem para formular hipótese, em especial a de que tirar diacrítico pode não baratear o texto nos vocabulários que já aprenderam a palavra acentuada.

## O que este manifesto não afirma

- Que a ABNT seja um modo de escrever prompt.
- Que voz culta gaste menos tokens do que voz simples.
- Que acento seja o principal custo, ou que removê-lo seja neutro para a qualidade.
- Que traduzir o prompt para o inglês seja sempre o melhor negócio.
- Que um piloto de doze textos prove uma lei do português.

As hipóteses operacionais estão em `HIPOTESES.md`. O modo de medi-las está em `docs/metodologia.md`. A comparação entre português brasileiro e inglês, modelo a modelo, está em `docs/benchmark-ptbr-en.md`. A escrita recomendada, com o grau de evidência de cada conselho, está em `docs/guia-de-escrita-ptbr.md`. As formas para copiar, por tipo de tarefa do piloto, estão em `docs/padroes-de-prompt.md`. A seção para quem precisa ser exato em português, com os métodos dos estudos e as práticas ABNT que cabem no pedido, está em `docs/escrita-precisa-ptbr.md`. O mesmo método, em skills para o agente, está em `skills/using-prompt-ptbr/SKILL.md`.
