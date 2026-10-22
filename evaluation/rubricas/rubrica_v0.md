# Rubrica v0

Versão registrada em 22 de outubro de 2026, antes de qualquer saída de modelo. Não ajuste pesos depois de ver respostas da mesma versão. Uma rubrica nova é `rubrica_v1.md`.

Aplica-se a cada resposta, com o texto-fonte e a instrução visíveis, e com o braço oculto para quem avalia.

| Critério | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Formato | Não cumpre o formato pedido | Cumpre em parte (JSON inválido, itens a mais ou a menos, texto extra) | Cumpre o formato pedido |
| Critérios explícitos | Ignora tamanho, campos ou frase obrigatória | Cumpre uma parte dos critérios explícitos | Cumpre os critérios explícitos da instrução |
| Fidelidade à fonte | Inventa fato decisivo ausente da fonte | Omite ou exagera um ponto sem inventar fato central | Usa só o que a fonte sustenta |
| Dado ausente | Afirma um valor quando a instrução mandava dizer que não consta | — | Responde a ausência como a instrução pediu, ou o caso não exigia essa regra |
| Idioma | A resposta útil não está no idioma pedido | Mistura idiomas na parte útil | Está no idioma pedido |

O traço na linha “dado ausente” evita nota intermediária: ou a regra de ausência se aplicava e foi cumprida, ou não se aplicava (os 2 pontos entram para não punir a tarefa), ou foi descumprida.

Nota bruta: soma, de 0 a 10. Não converta em “aprovado” sem declarar o corte numa versão posterior da rubrica, antes de olhar as notas.

Reprompt conta à parte: número de novos pedidos até o formato ficar utilizável, mais os tokens desses pedidos. Não some reprompt dentro da nota.

Quem avalia não vê o nome do braço. Uma amostra humana, mesmo pequena, acompanha qualquer juiz automático antes de o repositório falar em qualidade. A concordância entre humanos entra no relatório. Concordância baixa não é detalhe: é limite do que a nota significa.
