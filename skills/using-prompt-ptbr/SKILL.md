---
name: using-prompt-ptbr
description: >-
  Routes Brazilian Portuguese prompt work to the right skill before drafting.
  Use when writing, reviewing, shortening, or costing a prompt in Portuguese
  (PT-BR), or when the user mentions tokens, ABNT, precisão do pedido,
  custo de token, otimizar prompt, ASD-STE100, or linguagem controlada.
---

# Usar o plugin Prompt PT-BR

Se o pedido for escrever, revisar ou encurtar um prompt em português, invoque a skill correspondente antes de redigir.

Anuncie: `Using [skill] to [purpose]` e siga essa skill.

## Mapa

| Situação | Skill |
| --- | --- |
| Começo, ou o pedido ainda não diz qual peça usar | `using-prompt-ptbr` (esta) |
| Redigir ou reescrever o pedido | `writing-precise-ptbr` |
| Conferir se a redação pode ser chamada de otimizada | `checking-prompt` |
| Citação, referência, termo ou a sigla ABNT | `scoping-abnt` |
| ASD-STE100, STE, linguagem controlada ou “80%” | `docs/ste-escopo.md` e `HIPOTESES-v1.md`; não trate a sigla como economia de token |
| Contar tokens, comparar idiomas ou estimar dólar | `measuring-tokens` |

## Ordem

1. `writing-precise-ptbr` para produzir o texto.
2. `checking-prompt` antes de entregar como versão otimizada.
3. `scoping-abnt` se o pedido cita obra, norma ou dado externo.
4. `measuring-tokens` só se a pessoa pediu contagem ou custo. Não conte por iniciativa para “provar” economia.

## Paradas

- A ABNT não é técnica de reduzir token.
- O ASD-STE100 também não é. Não peça “escreva em STE” para encurtar, e não declare conformidade com o dicionário.
- Não recomende tirar acento.
- Não troque termo técnico por sinônimo mais curto.
- Não copie razão de tokens de Claude, Gemini ou Sabiá a partir de outro tokenizador.
- Não apresente 22,9%, 1,13×, 2,5% ou 5,5% como lei. São contagens deste repositório.
- Prompt mais curto por ter apagado critério é o braço vago, não o otimizado.
