# module08 — The Matrix: Welcome to the Real World of Data Engineering

Material de estudo (TL;DR + aprofundamento por conceito): [`concept.md`](concept.md).

## Estrutura

O subject não desenha uma árvore de arquivos explícita — cada capítulo de
exercício só define o diretório (`ex0/`, `ex1/`, `ex2/`) e os arquivos a
submeter. Cada exercício é independente dos outros: nenhum importa código
de outro.

```
module08/
├── ex0/
│   └── construct.py          # detecta venv, mostra info do ambiente Python
├── ex1/
│   ├── loading.py            # analise de dados: numpy -> pandas -> matplotlib
│   ├── requirements.txt      # dependencias no formato pip
│   └── pyproject.toml        # as MESMAS dependencias no formato Poetry
└── ex2/
    ├── oracle.py             # config via variaveis de ambiente + python-dotenv
    ├── .env.example          # template das 5 chaves (valores placeholder), versionado
    └── .gitignore            # ignora o .env real (nunca o .env.example)
```

O `matrix_env/` de cada exercício (o virtual environment criado durante o
teste/review) e o `matrix_analysis.png` gerado pelo `ex1` ficam fora do
repositório — ver `.gitignore` na raiz.

## Partes do subject

| Exercício | Arquivo | Conceito principal |
|-----------|---------|---------------------|
| ex0 — The Construct | `construct.py` | *virtual environment*: um ambiente Python isolado; o programa se inspeciona (`sys`, `site`) para saber se está dentro ou fora de um, e imprime saídas diferentes |
| ex1 — Loading Programs | `loading.py` + `requirements.txt` + `pyproject.toml` | *gerência de dependências*: importar libs de terceiros com degradação limpa quando faltam; declarar as mesmas deps nos dois formatos (pip e Poetry) |
| ex2 — The Oracle | `oracle.py` + `.env.example` + `.gitignore` | *configuração por ambiente*: ler config de env vars / arquivo `.env` (via `python-dotenv`), variar comportamento dev/prod, manter segredos fora do controle de versão |

## Rodando

```bash
# ex0 - fora e dentro de um venv (saidas diferentes)
python module08/ex0/construct.py
python -m venv module08/ex0/matrix_env
module08/ex0/matrix_env/Scripts/activate      # ...\Scripts\activate no Windows
python module08/ex0/construct.py

# ex1 - sem deps mostra instrucoes; com deps gera o PNG
python module08/ex1/loading.py                 # caminho "falta dependencia"
python -m venv module08/ex1/matrix_env
module08/ex1/matrix_env/Scripts/pip install -r module08/ex1/requirements.txt
module08/ex1/matrix_env/Scripts/python module08/ex1/loading.py

# ex2 - tres cenarios de config
python module08/ex2/oracle.py                                   # sem .env -> warnings
cp module08/ex2/.env.example module08/ex2/.env
python module08/ex2/oracle.py                                   # le do .env
MATRIX_MODE=production API_KEY=x DATABASE_URL=y python module08/ex2/oracle.py  # shell vence o .env
```

```bash
uv run flake8 module08/        # lint em todo o modulo
uv run mypy module08/ex0/construct.py module08/ex2/oracle.py
```

No `ex1`, o subject permite erros de `flake8`/`mypy` **apenas** relacionados
a import (as libs são opcionais e importadas sob `try/except`). Os outros
dois exercícios ficam limpos nas duas ferramentas.
