# Checklist de prompt

Use antes de tratar um prompt como versão otimizada. A lista não prova qualidade de resposta. As formas por tipo de tarefa estão em `docs/padroes-de-prompt.md`. O método longo, para quem precisa ser exato em português, está em `docs/escrita-precisa-ptbr.md`.

- [ ] A primeira frase diz a tarefa, no imperativo.
- [ ] O texto-fonte está separado da instrução por um rótulo.
- [ ] Dá para verificar se a resposta cumpriu o pedido: quantidade, tamanho, campos ou frase obrigatória.
- [ ] O idioma da resposta está explícito.
- [ ] Há uma regra para dado ausente, quando a tarefa puder ser verificada contra a fonte.
- [ ] Cortesia e preâmbulo foram removidos, ou transformados em regra de tom.
- [ ] Os diacríticos do português estão corretos.
- [ ] Nenhum termo do domínio foi trocado por um sinônimo “mais curto” sem decisão de glossário.
- [ ] Se a instrução foi traduzida do inglês, a resposta pedida continua no idioma de quem vai lê-la.
- [ ] O tokenizador usado na conta é o do modelo que vai receber o prompt, não um número emprestado de outro vocabulário.

Para comparar duas redações do mesmo pedido, os critérios verificáveis precisam estar nas duas. Se uma versão só é mais curta porque esqueceu uma regra, ela não é o braço otimizado: é o braço vago.
