# Prova de conceito

`01_tokenizacao.py` conta os braços do piloto de hipóteses.

`02_benchmark_modelos.py` compara português brasileiro e inglês no tokenizador de cada modelo do catálogo `benchmarks/datasets/modelos_v0.json`.

Não há notebook nesta versão. O script roda igual em CI e não depende de célula executada à mão. Um notebook, se entrar depois, deve chamar este arquivo em vez de copiar a contagem.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python poc/01_tokenizacao.py
.venv/bin/python poc/02_benchmark_modelos.py
```
