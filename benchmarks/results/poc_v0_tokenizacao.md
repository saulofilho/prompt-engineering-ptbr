# Piloto v0 — contagem de tokens

Resultado gerado por `poc/01_tokenizacao.py`. Não edite este arquivo à mão: rode o script de novo.

Este piloto descreve o conjunto v0. Não é estimativa populacional, não tem teste de hipótese confirmatório e não mede qualidade de resposta.

- Dataset: `2e0268f9b8be6672af5dec581c5ae603da05162e398d8bdd3019bf8ee4e4d210`
- Hipóteses: `a391c4b158622db6a9708e15513b72d1dfc8cacf1f88c6555f73bc16d4154b45`
- Léxico: `aab9f99c8e6cafc2f5988e7992ce137c0668c9915283bb16b8352c73ab70975c`
- Itens: 12
- Encoding da decisão: `o200k_base`

A soma de instrução e payload não precisa fechar com o prompt completo. O tokenizador de subpalavras pode fundir ou cortar a fronteira quando os trechos são concatenados. Cada escopo foi contado no texto que de fato o representa.

## Decisão no conjunto, encoding primário

- H1, instrução, redução de `pt_otimizado` frente a `pt_coloquial`: 22,9%. compativel com H1 neste conjunto.
- H3, prompt completo, razão `pt_paralelo` / `en`: 1,128. compativel com H3 neste conjunto.
- H5, prompt completo, redução ao remover diacríticos: -2,5%. compativel com H5 neste conjunto.

H2 e H4 não foram testadas. `pt_vago` pode gastar menos tokens porque apaga critérios; isso não é economia útil.

## Somas — o200k_base

| Braço | Instrução | Payload | Completo | Palavras | Caracteres | Tokens/palavra | Caracteres/token |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| EN | 437 | 459 | 896 | 658 | 3825 | 1,36 | 4,27 |
| PT paralelo | 490 | 521 | 1011 | 681 | 3935 | 1,48 | 3,89 |
| PT coloquial | 632 | 521 | 1153 | 802 | 4553 | 1,44 | 3,95 |
| PT vago | 72 | 521 | 593 | 407 | 2230 | 1,46 | 3,76 |
| PT otimizado | 487 | 521 | 1020 | 694 | 3895 | 1,47 | 3,82 |
| PT sem diacrítico | 495 | 539 | 1046 | 694 | 3895 | 1,51 | 3,72 |

## Contrastes — o200k_base

A coluna da esquerda é o primeiro braço do contraste. Redução positiva significa que a esquerda gastou menos tokens que a direita.

| Contraste | Escopo | Tokens à esquerda | Tokens à direita | Razão | Redução | Razão de caracteres | Tokens além do comprimento |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| otimizado / coloquial | instrucao | 487 | 632 | 0,771 | 22,9% | 0,749 | 1,029 |
| otimizado / coloquial | completo | 1020 | 1153 | 0,885 | 11,5% | 0,855 | 1,034 |
| paralelo / en | instrucao | 490 | 437 | 1,121 | -12,1% | 1,021 | 1,098 |
| paralelo / en | completo | 1011 | 896 | 1,128 | -12,8% | 1,029 | 1,097 |
| sem diacrítico / otimizado | completo | 1046 | 1020 | 1,025 | -2,5% | 1,000 | 1,025 |
| vago / otimizado | instrucao | 72 | 487 | 0,148 | 85,2% | 0,151 | 0,979 |

“Tokens além do comprimento” é a razão de tokens dividida pela razão de caracteres. Valor perto de 1 indica que a diferença de tokens acompanha o tamanho do texto. Valor acima de 1 indica fragmentação adicional.

## Instruções por tarefa — o200k_base

A redução é da instrução otimizada frente à coloquial. A coluna “Sem diacrítico” é o prompt completo, não a instrução.

| Tarefa | Coloquial | Otimizado | Redução | Paralelo | EN | Vago | Sem diacrítico |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| resumo-chamados | 63 | 31 | 50,8% | 31 | 29 | 7 | 100 |
| resumo-ata | 58 | 26 | 55,2% | 27 | 26 | 7 | 89 |
| extrair-chamado | 50 | 31 | 38,0% | 36 | 31 | 7 | 75 |
| extrair-cobranca | 51 | 36 | 29,4% | 36 | 33 | 7 | 91 |
| classificar-avaliacoes | 41 | 32 | 22,0% | 33 | 31 | 7 | 75 |
| classificar-incidentes | 72 | 64 | 11,1% | 65 | 58 | 5 | 106 |
| codigo-media-movel | 53 | 45 | 15,1% | 43 | 38 | 7 | 72 |
| codigo-validar-cpf | 53 | 51 | 3,8% | 48 | 35 | 6 | 75 |
| escolher-fornecedor | 53 | 39 | 26,4% | 39 | 36 | 5 | 110 |
| verificar-prazo | 44 | 42 | 4,5% | 42 | 38 | 5 | 82 |
| qa-abertura | 46 | 44 | 4,3% | 44 | 38 | 6 | 81 |
| qa-tarifa | 48 | 46 | 4,2% | 46 | 44 | 3 | 90 |

## Somas — cl100k_base

| Braço | Instrução | Payload | Completo | Palavras | Caracteres | Tokens/palavra | Caracteres/token |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| EN | 445 | 460 | 905 | 658 | 3825 | 1,38 | 4,23 |
| PT paralelo | 568 | 600 | 1168 | 681 | 3935 | 1,72 | 3,37 |
| PT coloquial | 746 | 600 | 1346 | 802 | 4553 | 1,68 | 3,38 |
| PT vago | 93 | 600 | 693 | 407 | 2230 | 1,70 | 3,22 |
| PT otimizado | 578 | 600 | 1190 | 694 | 3895 | 1,71 | 3,27 |
| PT sem diacrítico | 583 | 604 | 1199 | 694 | 3895 | 1,73 | 3,25 |

## Contrastes — cl100k_base

Secundário. Não decide H1, H3 nem H5.

| Contraste | Escopo | Tokens à esquerda | Tokens à direita | Razão | Redução | Razão de caracteres | Tokens além do comprimento |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| otimizado / coloquial | instrucao | 578 | 746 | 0,775 | 22,5% | 0,749 | 1,035 |
| otimizado / coloquial | completo | 1190 | 1346 | 0,884 | 11,6% | 0,855 | 1,033 |
| paralelo / en | instrucao | 568 | 445 | 1,276 | -27,6% | 1,021 | 1,250 |
| paralelo / en | completo | 1168 | 905 | 1,291 | -29,1% | 1,029 | 1,255 |
| sem diacrítico / otimizado | completo | 1199 | 1190 | 1,008 | -0,8% | 1,000 | 1,008 |
| vago / otimizado | instrucao | 93 | 578 | 0,161 | 83,9% | 0,151 | 1,066 |

## Fragmentação de formas

Cada célula lista as peças, separadas por `·`. “Com espaço” é a forma no meio de uma frase, com o espaço que o pré-tokenizador costuma colar na palavra. A grafia sem diacrítico está aqui para ser observada. Não é modelo de escrita.

| Forma | o200k isolada | o200k com espaço | cl100k isolada | cl100k com espaço |
| --- | --- | --- | --- | --- |
| `ação` | ação |  ação | ação |  a · ção |
| `acao` | acao |  ac · ao | acao |  a · cao |
| `informação` | inform · ação |  informação | inform · ação |  inform · ação |
| `informacao` | inform · acao |  inform · acao | inform · acao |  inform · acao |
| `configuração` | config · uração |  configuração | config · ura · ção |  config · ura · ção |
| `configuracao` | config · ur · acao |  configur · acao | config · ur · acao |  configur · acao |
| `implementação` | implement · ação |  implementação | implement · ação |  implement · ação |
| `implementacao` | implement · acao |  implement · acao | implement · acao |  implement · acao |
| `requisição` | requ · isição |  requ · isição | re · quis · ição |  requ · isi · ção |
| `requisicao` | re · quis · icao |  requis · icao | re · quis · icao |  requis · icao |
| `não` | não |  não | n · ão |  não |
| `nao` | na · o |  nao | na · o |  nao |
| `você` | v · ocê |  você | v · ocê |  você |
| `voce` | vo · ce |  voce | vo · ce |  vo · ce |
| `usuário` | usu · ário |  usuário | usu · ário |  usuário |
| `usuario` | usuario |  usuario | usuario |  usuario |
| `resuma` | res · uma |  res · uma | res · uma |  res · uma |
| `escreva` | es · cre · va |  escre · va | es · cre · va |  escre · va |
| `classifique` | class · ifique |  class · ifique | class · ifique |  class · ifique |
| `extraia` | extra · ia |  extra · ia | extra · ia |  extra · ia |
| `poderia` | p · oder · ia |  poderia | p · oder · ia |  poder · ia |
| `por favor` | por ·  favor |  por ·  favor | por ·  favor |  por ·  favor |

## Leitura que este arquivo não autoriza

- Não autoriza dizer que a ABNT economiza tokens.
- Não autoriza remover acento como prática.
- Não autoriza concluir que o prompt otimizado responde melhor. Qualidade não foi medida.
- Não autoriza transportar o prêmio deste conjunto para outro corpus ou outro tokenizador.

