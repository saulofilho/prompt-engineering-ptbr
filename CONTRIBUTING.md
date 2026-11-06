# Como contribuir

## O que cabe aqui

- Par de prompts com o mesmo critério nos braços que se pretende comparar, e marcadores que o script consiga verificar.
- Tokenizador novo, com versão fixada e contagem reprodutível.
- Correção de citação, com a fonte aberta.
- Rubrica ou amostra humana da fase de qualidade, quando ela existir, no desenho de `HIPOTESES-v2.md` se a pergunta for omissão de critério.
- Tradução fiel de um item, identificada como outra versão de dataset.

## O que não cabe

- Script de ataque, jailbreak ou instrução para obter comportamento que o modelo recusa por segurança.
- Resultado de qualidade inventado, média sem os itens, ou tabela colada de outro corpus como se fosse deste.
- Edição dos limiares em `HIPOTESES.md` depois que `benchmarks/results/` existir para aquela versão. O v1 está em `HIPOTESES-v1.md` e o v2 em `HIPOTESES-v2.md`. Hipótese nova entra em `HIPOTESES-v3.md`.
- Resultado da H8 escrito em `HIPOTESES-v2.md`. Essa hipótese ainda não tem participante. Nota humana só decide a H8 com consentimento, lista de critérios anterior à redação e avaliador cego, como em `evaluation/humanos/README.md`.
- Recomendação de remover diacrítico ou de trocar termo técnico por sinônimo mais barato, sem um experimento que separe sentido e token.

## Dataset

Cada item precisa de `en`, `pt_paralelo`, `pt_coloquial`, `pt_vago` e `pt_otimizado`, mais as fontes nos dois idiomas. Os marcadores de `pt_coloquial` e `pt_otimizado` são os mesmos. `pt_vago` não pode contê-los todos. Rode `python3 tools/validar_dataset.py` para a forma e `poc/01_tokenizacao.py --checar` para os marcadores antes de abrir a discussão dos números.

## Antes de abrir o pull request

As mesmas verificações do CI (ver [`.github/workflows/ci.yml`](.github/workflows/ci.yml)):

```bash
python3 tools/sync_skills.py --check
python3 tools/validar_dataset.py
.venv/bin/python poc/01_tokenizacao.py --checar
.venv/bin/python evaluation/automatico/checagem_v0.py
.venv/bin/ruff check .
.venv/bin/pytest
```

Se você mexeu em uma skill, edite só `skills/` e rode `python3 tools/sync_skills.py` para atualizar `.cursor/skills/`.

Não descreva o próprio nome civil de outra pessoa a partir de um usuário de rede. Exemplos do dataset usam figuras fictícias.

## Texto

Português brasileiro com diacríticos. Referências novas seguem o padrão de `docs/referencias.md`. Afirmação quantitativa aponta o arquivo gerado e o hash, ou a publicação externa. Blogue entra como blogue.

## Conduta

`CODE_OF_CONDUCT.md` vale para issue, pull request e revisão.
