---
name: writing-precise-ptbr
description: >-
  Rewrites a prompt into precise Brazilian Portuguese: imperative task,
  numbered checkable rules, one stable term, exact missing-data phrase,
  and answer language. Use when the user asks to write, rewrite, or tighten
  a PT-BR prompt.
---

# Escrever prompt preciso em português

Siga esta ordem. Não alongue com cortesia. Não apague critério para encurtar.

1. Tarefa, numa frase no imperativo: Resuma, Extraia, Classifique, Liste, Escreva.
2. Regras numeradas. Cada uma tem de ser conferível. “Seja claro” não entra.
3. Definição única do termo que não pode oscilar.
4. Se o dado puder faltar na fonte, a frase exata. Padrão: `responda exatamente: não informado`.
5. Idioma e formato: `Responda em português brasileiro.`
6. Fonte num bloco com rótulo (`Texto:`, `Dados:`, `Contexto:`), separada da instrução.
7. Um exemplo mínimo só se a regra ainda couber em duas leituras.

Tom, se for requisito, vira regra (`tom formal, sem saudação`), não preâmbulo.

## Modelo

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

## Entrega

Devolva o prompt reescrito. Se mudou o sentido para encurtar, diga o que saiu. Não chame a versão de otimizada antes de `checking-prompt`.

Os padrões por tipo de tarefa estão em `docs/padroes-de-prompt.md`. O método longo e o lastro dos estudos estão em `docs/escrita-precisa-ptbr.md`. Se o pedido citar ASD-STE100, STE ou “80%”, leia `docs/ste-escopo.md` antes de reescrever.
