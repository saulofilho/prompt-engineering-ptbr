# Metodologia

## Pergunta

Para um mesmo objetivo, quanto da diferença de tokens entre inglês e português, e entre um português verboso e um português enxuto, vem do empacotamento, do comprimento do texto e da fragmentação do tokenizador? Quanto disso sobrevive quando a resposta tem de sair em português e o payload é grande?

O piloto v0 responde só à primeira metade, e apenas no conjunto escrito para o experimento.

## Braços

| Braço | O que segura constante | O que varia |
| --- | --- | --- |
| `en` | Critérios da tarefa e pedido de resposta em português brasileiro | Inglês idiomático |
| `pt_paralelo` | Os mesmos critérios, em tradução próxima do inglês | Português |
| `pt_coloquial` | Os mesmos marcadores de critério do braço otimizado | Cortesia, conectivo e volta |
| `pt_otimizado` | Os mesmos marcadores | Imperativo, lista e ausência de cortesia |
| `pt_vago` | O objetivo geral | Omissão deliberada dos critérios |
| `pt_sem_acento` | O texto otimizado | Diacríticos removidos por NFKD |

`pt_coloquial` e `pt_otimizado` não podem ser comparados se um deles esqueceu uma regra. O script recusa o conjunto quando um marcador obrigatório some. `pt_vago` é o braço da hipótese de qualidade (H2). Token menor nesse braço é esperado e não conta como vitória.

O braço inglês pede a resposta em português brasileiro. Sem esse controle, uma economia na entrada se mistura com outra tarefa: responder em inglês.

## Três escopos

Cada item é contado três vezes:

- **Instrução:** o pedido, sem o texto-fonte.
- **Payload:** rótulo e texto-fonte.
- **Completo:** instrução, linha em branco, rótulo e texto-fonte, como o modelo receberia.

A contagem de subpalavras não é aditiva. A fronteira entre instrução e payload pode fundir peças. Por isso o completo é contado no texto concatenado, e não obtido pela soma.

H1 olha a instrução. Se o payload for longo, a mesma economia pesa pouco no completo. O relatório mostra os dois escopos para essa leitura não se perder.

## Métricas

- Tokens, palavras (separadas por espaço), caracteres Unicode em NFC e bytes UTF-8.
- Fertilidade: tokens por palavra, na razão das somas.
- Caracteres por token.
- Prêmio: tokens do braço A divididos pelos tokens do braço B.
- Decomposição: prêmio de tokens dividido pelo prêmio de caracteres. Perto de 1, a diferença acompanha o tamanho. Acima de 1, há fragmentação além do comprimento.

Não há preço em moeda no v0. Quando houver, o preço entra como tabela datada, externa ao resultado, multiplicada pelos tokens de entrada e de saída. Trocar a tabela não reescreve a contagem.

## Agregação e decisão

A decisão usa a razão das somas no `o200k_base`. A média das razões por item daria o mesmo peso a uma instrução de oito tokens e a uma de oitenta. A mediana por item aparece no detalhe, não na decisão.

Os limiares estão em `HIPOTESES.md` e não são reestimados depois da contagem. Com doze itens escritos pelo projeto, “compatível com a hipótese neste conjunto” não é confirmação estatística. Não há valor-p neste piloto. Um n de centenas, com teste pareado, intervalo bootstrap e correção para hipóteses múltiplas, fica para a fase em que o conjunto não for desenhado pela mesma pessoa que lê o resultado.

## Tokenizadores

O piloto de hipótese (H1, H3, H5) usa tiktoken: `o200k_base` para a decisão e `cl100k_base` como secundário. São vocabulários da OpenAI, não um modelo genérico de “LLM”.

A comparação entre famílias está em `docs/benchmark-ptbr-en.md`. Lá, cada linha é o tokenizador publicado daquele modelo (Llama, Gemma, Qwen, DeepSeek, Mistral, além dos dois encodings da OpenAI), com `add_special_tokens` desligado. Claude, Gemini e Sabiá ficam na mesma tabela sem número: aproximar esses bots por outro vocabulário seria outro experimento, e seria rotulado como aproximação. A contagem válida, quando o tokenizador não é público, é o endpoint do provedor no modelo exato.

## Fase de qualidade, ainda não executada

Quando houver chamada de modelo, o desenho mínimo é:

- os mesmos braços e o mesmo idioma de resposta;
- temperatura 0 nas tarefas de extração, classificação e resposta verificável; 0,2 em resumo e geração;
- três repetições por item e por modelo;
- ao menos um modelo de API comercial, um modelo aberto multilíngue e, se a API existir, um modelo com treino forte em português;
- rubrica `evaluation/rubricas/rubrica_v0.md`, congelada antes das saídas;
- juízo automático apenas como triagem, com amostra humana cega;
- custo do fluxo = entrada + saída + reprompts usados para cumprir o formato.

Araújo (2025) registrou concordância humana baixa na avaliação de respostas. Um juiz automático único, sobretudo se favorecido pelo inglês, não fecha a H2 nem a H4.

## Ameaças à validade do v0

- Os textos foram escritos para o estudo. A cortesia da variante coloquial é artificial, embora os critérios estejam literalmente presentes.
- n = 12. Um item longo pode puxar a soma.
- Só dois vocabulários da mesma família.
- Nas tarefas de código, o nome da função foi localizado. Parte do prêmio é o identificador, não a prosa.
- Tradução própria. Outro redator produziria outro comprimento.
- Marcadores idênticos tornam o coloquial menos natural do que um pedido real.
- Não há amostra de produção, de chat nem de sistema com milhares de tokens de contexto.
- O léxico de fragmentação usa palavras isoladas. Palavra isolada e palavra no meio da frase não tokenizam igual; o relatório mostra as duas.

## O que não fazer com o resultado

Não promover o percentual do piloto a “o português custa X% a mais”. Não recomendar a variante vaga porque ela é curta. Não citar este repositório como prova de qualidade de resposta até que a fase de qualidade exista e os hashes batam com as hipóteses daquela versão.

## Versão v1

H6 e H7 estão em `HIPOTESES-v1.md`. O braço `pt_controlado` repete os marcadores do otimizado, com no máximo 20 palavras por segmento, e não pede a sigla ASD-STE100. A contagem está em `benchmarks/results/poc_v1_controlado.md`. H7 registra o estímulo de três formatos de saída e não tem token de resposta enquanto a API não devolver o `usage`.
