# Hipóteses pré-registradas, versão v2

Versão: v2  
Data de registro: 4 de novembro de 2026  
Estado: desenho registrado antes de qualquer participante e antes de qualquer nota em `evaluation/humanos/`.

Não edite o desfecho, as condições nem a regra de “ambíguo” depois que existir redação de participante. Um ajuste entra em arquivo de versão seguinte. O v0 e o v1 não são reabertos aqui.

## Recorte

H8 é uma hipótese sobre quem escreve o prompt. Não é hipótese de token, de qualidade de resposta nem de mecanismo interno do modelo. A literatura que a torna plausível está em `docs/mente-de-quem-escreve.md`. Essa literatura não é o teste.

Não há dado. Não escreva resultado neste arquivo.

## Definições

- **Critério necessário.** Item de uma lista fechada antes da redação. Sem ele, a tarefa não se executa nem se confere conforme a especificação.
- **Omissão.** O avaliador marca o critério como ausente. Marca ambígua não conta como presente e entra no relatório à parte. Não entra no numerador do desfecho primário.
- **Externalização.** A condição em que a lista fechada está visível para quem escreve.
- **Unidade de análise.** Um prompt produzido por uma pessoa, numa condição.
- **Unidade de observação.** O par pessoa-critério.

## Condições

A mesma tarefa nas duas condições. A designação é definida antes da sessão.

| Condição | O que a pessoa recebe |
| --- | --- |
| Escrita livre | A tarefa, sem a lista de critérios |
| Lista fechada | A tarefa e a lista de critérios necessários, à vista |

Quem avalia não sabe a condição. A lista de critérios que os avaliadores usam é a mesma lista fechada, também fixada antes das redações.

## H8 — Externalização e omissão

Na amostra deste desenho, a proporção de critérios necessários marcados como ausentes é menor na condição de lista fechada do que na condição de escrita livre.

A proporção é a soma das ausências dividida pela soma dos pares pessoa-critério, não a média das proporções por pessoa. Proporção menor na lista fechada é compatível com H8 nesta amostra. Proporção igual ou maior recusa H8 nesta amostra. Não há limiar de diferença mínima nesta versão: o desfecho é de direção. Não há valor-p. Com amostra desenhada pelo próprio projeto, o desfecho é descritivo.

O token do prompt produzido pode ser contado como análise secundária, no tokenizador do modelo nomeado antes da sessão. Essa conta não decide H8. A H6 já mostrou, noutro contraste e sem participante, que uma forma mais explícita pode gastar mais tokens de instrução. H8 não herda esse número e não o trata como previsão obrigatória.

## O que precisa existir antes de recolher dado

- Consentimento de quem escreve e de quem avalia.
- A lista fechada de critérios, com data anterior à primeira redação.
- Regra de exclusão de redação incompleta, escrita antes da sessão.
- Ocultação da condição para quem avalia.

Sem esses quatro itens, H8 permanece desenho. Nota solta em `evaluation/humanos/` não a decide.

## O que a v2 não decide

- Se o modelo responde melhor quando o critério está no texto. Isso continua a H2, sem nota.
- Carga cognitiva, maldição do conhecimento como estado mental medido, ou ideologia linguística como variável.
- Qualidade, tom ou preferência.
- Token de Claude, Gemini ou Sabiá sem a contagem da API daquele modelo.
