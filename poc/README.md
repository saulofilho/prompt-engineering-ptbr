# Prova de conceito

O piloto executável é `01_tokenizacao.py`. Ele lê `benchmarks/datasets/pares_v0.json` e grava `benchmarks/results/`.

Não há notebook nesta versão. O script roda igual em CI e não depende de célula executada à mão. Um notebook, se entrar depois, deve chamar este arquivo em vez de copiar a contagem.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python poc/01_tokenizacao.py
```
