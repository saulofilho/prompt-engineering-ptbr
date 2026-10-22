# Prova de conceito

`01_tokenizacao.py` conta os braços do piloto de hipóteses.

`02_benchmark_modelos.py` compara português brasileiro e inglês no tokenizador de cada modelo do catálogo.

`03_custo.py` converte esses tokens em dólar com a tabela datada.

`04_gerar_e_avaliar.py` chama os modelos, mede formato, alucinação verificável e reprompt, e só publica a razão de Claude, Gemini ou Sabiá quando a API devolve a contagem.

Não há notebook nesta versão. O script roda igual em CI e não depende de célula executada à mão. Um notebook, se entrar depois, deve chamar este arquivo em vez de copiar a contagem.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python poc/01_tokenizacao.py
.venv/bin/python poc/02_benchmark_modelos.py
.venv/bin/python poc/03_custo.py
.venv/bin/python poc/04_gerar_e_avaliar.py
```
