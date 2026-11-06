# Política de segurança

Este é um repositório de pesquisa: scripts de contagem de tokens, datasets de
prompts e um plugin de skills. Não há serviço em produção nem dados de pessoas.

## Escopo

- **Chaves de API.** Os scripts leem chaves só de variável de ambiente
  (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`/`GOOGLE_API_KEY`,
  `MARITACA_API_KEY`/`SABIA_API_KEY`). Nenhuma chave é gravada em resultado,
  log ou commit. Não envie chave no corpo de uma issue ou pull request.
- **Sem segredo versionado.** `.env` está no `.gitignore`. Se um segredo vazar
  num commit, rode a rotação da chave no provedor antes de qualquer outra coisa.
- **Conteúdo que não cabe (ver `CONTRIBUTING.md`).** Não aceitamos script de
  ataque, jailbreak ou instrução para obter comportamento que o modelo recusa
  por segurança. Prompts do dataset usam figuras fictícias e não descrevem o
  nome civil de uma pessoa a partir de um usuário de rede.

## Como relatar

Para uma vulnerabilidade ou um vazamento de segredo neste repositório, abra uma
issue sem dados sensíveis, ou use o canal privado de *security advisory* do
GitHub em **Security → Report a vulnerability**. Descreva o impacto e um passo a
passo de reprodução. Resposta esperada em até duas semanas.
