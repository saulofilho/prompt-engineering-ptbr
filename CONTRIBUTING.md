# Como contribuir

## O que cabe aqui

- Par de prompts com o mesmo critério nos braços que se pretende comparar, e marcadores que o script consiga verificar.
- Tokenizador novo, com versão fixada e contagem reprodutível.
- Correção de citação, com a fonte aberta.
- Rubrica ou amostra humana da fase de qualidade, quando ela existir.
- Tradução fiel de um item, identificada como outra versão de dataset.

## O que não cabe

- Script de ataque, jailbreak ou instrução para obter comportamento que o modelo recusa por segurança.
- Resultado de qualidade inventado, média sem os itens, ou tabela colada de outro corpus como se fosse deste.
- Edição dos limiares em `HIPOTESES.md` depois que `benchmarks/results/` existir para aquela versão. Abra `HIPOTESES-v1.md`.
- Recomendação de remover diacrítico ou de trocar termo técnico por sinônimo mais barato, sem um experimento que separe sentido e token.

## Dataset

Cada item precisa de `en`, `pt_paralelo`, `pt_coloquial`, `pt_vago` e `pt_otimizado`, mais as fontes nos dois idiomas. Os marcadores de `pt_coloquial` e `pt_otimizado` são os mesmos. `pt_vago` não pode contê-los todos. Rode `poc/01_tokenizacao.py --checar` antes de abrir a discussão dos números.

Não descreva o próprio nome civil de outra pessoa a partir de um usuário de rede. Exemplos do dataset usam figuras fictícias.

## Texto

Português brasileiro com diacríticos. Referências novas seguem o padrão de `docs/referencias.md`. Afirmação quantitativa aponta o arquivo gerado e o hash, ou a publicação externa. Blogue entra como blogue.

## Conduta

`CODE_OF_CONDUCT.md` vale para issue, pull request e revisão.
