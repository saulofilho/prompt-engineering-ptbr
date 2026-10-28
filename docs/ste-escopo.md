# O que o ASD-STE100 faz neste projeto

O ASD-STE100 (Simplified Technical English), Issue 9, de 15 de janeiro de 2025, é a especificação da ASD para manual técnico em inglês controlado. A origem é a manutenção de aeronave: o leitor muitas vezes não tem o inglês como primeira língua, e uma frase ambígua vira erro de procedimento. A especificação tem duas partes. A parte 1 é um conjunto de regras de escrita. A parte 2 é um dicionário de palavras gerais aprovadas, em geral uma palavra com um sentido e uma classe gramatical, mais nomes e verbos técnicos do domínio. A grafia de referência é o inglês americano. O texto oficial está em [asd-ste100.org](https://www.asd-ste100.org/). Este repositório não reproduz o dicionário.

Um pedido em português brasileiro não fica “em STE” porque alguém escreveu a sigla. O dicionário é inglês. Pedir a resposta nesse padrão empurra a entrega para fora do idioma que o piloto fixa.

## O que não fazer com a sigla

Chamar de STE um prompt curto, ou esperar que a sigla reduza token, repete o uso da ABNT como emblema. A regra 4.2 da própria especificação manda não omitir palavra nem usar contração para encurtar: frase mais curta não é frase mais fácil de ler. Isso está do lado da tese deste repositório, não do atalho.

“Cerca de 80% do caminho” não é regra da especificação. É um afrouxamento circulado a partir de um post de Andrej Karpathy, em 2 de outubro de 2026, sobre como ler a saída de um modelo. Sem dizer quais regras ficam, o percentual não se confere. Sem o dicionário oficial, o modelo não tem como cumprir o vocabulário, e uma frase que declara conformidade não a prova.

O post trata de entender a saída: prosa controlada, diagrama, página HTML e vídeo explicativo. Não mede token de entrada em português. Vídeo fica fora deste repositório até existir um roteiro com critério conferível. Compreensão de quem lê é amostra humana, em `evaluation/humanos/`, não contagem de token.

## O que a especificação empresta

Quatro regras contáveis viram critério em português. O braço que as aplica se chama `pt_controlado`. Ele não se declara conforme ao ASD-STE100.

| Regra, em paráfrase | No pedido em português |
| --- | --- |
| Uma instrução por frase. Duas ações entram na mesma frase só quando ocorrem juntas. | Cada exigência fica numa frase. “Revise o diff e corrija o teste” vira duas frases. |
| Procedimento no imperativo. | “Resuma”, “Extraia”, “Classifique”. A voz passiva não diz quem age. |
| Um nome para cada coisa, sempre o mesmo. | O bloco `Termo:` define a palavra. Sinônimo mais curto não substitui o termo. |
| No máximo 20 palavras numa frase de procedimento. | O script de v1 recusa a frase que passa disso. O teto é de conferência, não de economia. |
| Depois do passo que não mostra resultado, diga como conferir. | “Responda exatamente: não informado”, campo obrigatório, frase de tamanho máximo. |

A frase de procedimento neste braço também não corta palavra para caber no teto. Se a regra não cabe em 20 palavras, ela se divide. Não se telegrafa.

## Moldes de comunidade e filtro de frase

CARE, COAST e CO-STAR circulam como moldes para preencher contexto, objetivo, tom, público e formato. As expansões mudam conforme o autor. Este repositório não escolhe uma expansão como padrão. Não há par experimental desses moldes aqui.

| | Molde de comunidade | ASD-STE100 | Este repositório |
| --- | --- | --- | --- |
| O que organiza | Blocos do pedido: cenário, tarefa, público, tom | Frase e vocabulário do inglês técnico | Critério conferível no braço otimizado |
| O que se confere | O bloco foi preenchido | A regra e, na norma, a palavra aprovada | O marcador está no texto e a resposta tem formato verificável |
| De onde vem | Textos da comunidade de prompt | Especificação de manual de aeronave | Pares v0 e as hipóteses registradas |

O que os moldes têm e os pares v0 não têm é o leitor da resposta, quando essa pessoa não é quem escreve o pedido. Isso entra como campo opcional, não como framework:

```text
Público:
- [quem lê a resposta]
```

Tom continua como regra (“tom formal, sem saudação”), no mesmo lugar em que a cortesia deixou de ser preâmbulo.

## Onde isso está no estudo

- Hipóteses da forma controlada e do formato de saída: `HIPOTESES-v1.md`. O arquivo `HIPOTESES.md` permanece o registro v0.
- Braço `pt_controlado`: `benchmarks/datasets/pares_v1_controlado.json`.
- Estímulos de formato, ainda sem chamada de modelo: `benchmarks/datasets/formatos_v1.json`.
- Padrões para copiar: `docs/padroes-de-prompt.md`.
- Escopo da ABNT, o paralelo desta página: `docs/abnt-escopo.md`.
