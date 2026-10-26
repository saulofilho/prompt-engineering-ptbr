---
name: checking-prompt
description: >-
  Checks a Brazilian Portuguese prompt against the precision checklist before
  calling it optimized. Use when reviewing a PT-BR prompt, comparing two
  wordings, or deciding whether a shorter version dropped a rule.
---

# Conferir o prompt

Leia o prompt inteiro. Marque cada item como cumpre ou falha. Não invente nota de qualidade de resposta.

- [ ] A primeira frase diz a tarefa, no imperativo.
- [ ] A fonte está separada da instrução por um rótulo.
- [ ] Dá para verificar o cumprimento: quantidade, tamanho, campos ou frase obrigatória.
- [ ] O idioma da resposta está explícito.
- [ ] Há regra para dado ausente, quando a tarefa puder ser checada contra a fonte.
- [ ] Cortesia e preâmbulo saíram, ou viraram regra de tom.
- [ ] Os diacríticos estão corretos.
- [ ] Nenhum termo do domínio foi trocado por sinônimo mais curto.
- [ ] Se a instrução está em inglês, a resposta pedida continua em português brasileiro.

## Duas redações

Os critérios conferíveis precisam estar nas duas. Se uma só é mais curta porque esqueceu uma regra, nomeie-a como vaga, não como otimizada.

## Saída

Liste os itens que falharam, em uma linha cada, e a correção mínima. Se nenhum falhou, diga que a redação passa no checklist. Isso não mede qualidade da resposta do modelo.
