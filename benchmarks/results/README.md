# Resultados

Os arquivos `poc_v0_tokenizacao.md` e `poc_v0_tokenizacao.json` são gerados por `poc/01_tokenizacao.py`.

`benchmark_modelos_ptbr_en.md` e `benchmark_modelos_ptbr_en.json` são gerados por `poc/02_benchmark_modelos.py`. Essa é a comparação entre português brasileiro e inglês, por família de modelo.

`custo_usd.md` é gerado por `poc/03_custo.py`.

`geracao_qualidade.md` e `benchmark_api_ptbr_en.md` são gerados por `poc/04_gerar_e_avaliar.py`.

`contagem_claude.json` é gerado por `poc/06_contar_tokens_claude.py` e `contagem_gemini.json` por `poc/07_contar_tokens_gemini.py`. Os dois também regravam `benchmark_api_ptbr_en.md`. O `04` preserva cada linha enquanto o modelo e o dataset forem os mesmos e não houver `usage`. O mesmo dataset em LF ou em CRLF conta como o mesmo.

`poc_v1_controlado.md` e `poc_v1_controlado.json` são gerados por `poc/05_controlado.py`.

Rode o script para criar ou atualizar. Não edite os números à mão.

## Dois hashes para `pares_v0.json`

O mesmo dataset aparece com dois SHA-256, porque o commit `d46f156` trocou a quebra de linha de LF para CRLF depois do resultado da v0. O conteúdo é o mesmo.

| Versão | Commit | SHA-256 | Registrada em |
| --- | --- | --- | --- |
| LF | `dff181f` | `2e0268f9b8be6672af5dec581c5ae603da05162e398d8bdd3019bf8ee4e4d210` | `poc_v0_tokenizacao` e `benchmark_modelos_ptbr_en` |
| CRLF, a atual | `d46f156` | `e8e0c771c7f49b117eb345e24e18f35f2a3418184e2f50cc46deadebb5606636` | `poc_v1_controlado.json` e `contagem_gemini.json` |

Para conferir, na raiz de um clone com histórico completo:

```bash
git show dff181f:benchmarks/datasets/pares_v0.json | shasum -a 256
git show d46f156:benchmarks/datasets/pares_v0.json | shasum -a 256
git diff --ignore-space-at-eol --stat dff181f HEAD -- benchmarks/datasets/pares_v0.json
```

Os dois primeiros comandos devolvem os hashes da tabela. O terceiro não mostra nada enquanto só a quebra de linha diferir.

Nenhum registro foi regravado para igualar os hashes: cada um descreve os bytes que existiam quando o script rodou. O `.gitattributes` mantém o arquivo em CRLF. Não o normalize. Rodar o `01` ou o `02` de novo grava o hash da versão atual no lugar do registro da v0, então não publique essa troca como se fosse o resultado original.
