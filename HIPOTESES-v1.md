# Hipóteses pré-registradas, versão v1

Versão: v1  
Data de registro: 28 de outubro de 2026  
Estado: registrada antes da contagem de `pt_controlado` e antes de qualquer chamada de modelo para formato de saída.

Não edite limiares, braços ou critérios deste arquivo depois de existir resultado em `benchmarks/results/poc_v1_controlado.md`. Uma hipótese nova entra em arquivo de versão seguinte. O v0 continua em `HIPOTESES.md` e não é reaberto aqui.

## Recorte

A v1 acrescenta dois objetos. H6 compara, no mesmo conjunto de doze tarefas, a instrução `pt_otimizado` com uma reescrita controlada. H7 compara formatos de saída e só pode ser decidida com o `usage` da API. Nenhum dos dois transforma o ASD-STE100 em dialeto de prompt nem em técnica de token.

Encoding da decisão de H6: `o200k_base`. O `cl100k_base` entra no relatório e não decide. Agregação: razão das somas. n = 12, textos escritos para o estudo. O desfecho é descritivo.

## Forma controlada

`pt_controlado` guarda cada marcador de `marcadores_pt` do item v0. Além disso, nesta versão:

- cada segmento, depois de cortar por linha e por ponto final, interrogação ou exclamação, tem no máximo 20 palavras separadas por espaço;
- o texto é diferente de `pt_otimizado`;
- o texto não pede a sigla ASD-STE100 e não declara conformidade com a especificação;
- o texto não traz cortesia de preâmbulo (`por favor`, `obrigado`, `obrigada`, `tudo bem`).

O teto de 20 palavras e a frase separada vêm da paráfrase das regras de procedimento do ASD-STE100. O dicionário inglês da especificação não é aplicado. Cumprir este braço não é cumprir a norma.

## H6 — Forma controlada e tokens de instrução

No conjunto v1, a soma dos tokens da instrução `pt_controlado` não é pelo menos 15% menor que a soma dos tokens da instrução `pt_otimizado` no `o200k_base`.

A redução é `1 - (tokens da instrução controlada / tokens da instrução otimizada)`, na soma dos doze itens. Redução igual ou superior a 15% recusa H6 neste conjunto. Redução menor, empate ou aumento é compatível com H6 neste conjunto.

O sinal esperado antes da contagem é ausência de corte grande. A especificação manda repetir o nome e proíbe omitir palavra para encurtar. Isso pode alongar a instrução. Alongar e ainda assim ficar compatível com H6 é o desfecho que a hipótese admite. Não é vitória de clareza: H6 não mede resposta.

A decisão usa só a instrução. O prompt completo, com o mesmo payload do v0, entra no relatório porque a contagem de subpalavras não é aditiva. Ele não troca o limiar.

## H7 — Formato da saída

A mesma pergunta, com o critério do braço otimizado, pede a resposta em um de três formatos: frases, diagrama Mermaid ou documento HTML. O idioma da resposta continua o português brasileiro.

Entram as tarefas em que o produto ainda é uma resposta em linguagem: `resumo-chamados`, `resumo-ata`, `escolher-fornecedor`, `verificar-prazo`, `qa-abertura`, `qa-tarifa`. Extração, classificação e código ficam de fora: trocar JSON ou código por diagrama seria outra tarefa.

A decisão, quando houver chamada, usa a soma dos tokens de saída que o provedor devolver, só nos itens em que a checagem de formato passar:

- frases: a resposta não contém uma cerca `mermaid` nem a marca `<html`;
- Mermaid: a resposta contém uma cerca `mermaid`;
- HTML: a resposta contém `<html` ou `<!DOCTYPE`.

Contagem local de entrada descreve o estímulo e não decide H7. Vídeo não é braço. Compreensão de quem lê não é H7: entra em `evaluation/humanos/`. Sem `usage` da API, a linha fica vazia.

## O que a v1 não decide

- Qualidade, alucinação, tom ou preferência humana da forma controlada.
- Conformidade com o dicionário ou com as 53 regras do ASD-STE100.
- Que “80%” seja um grau reproduzível.
- Custo em dólar dos formatos. Preço continua tabela datada, externa a este arquivo.
- Token de Claude, Gemini ou Sabiá sem a contagem da API daquele modelo.
