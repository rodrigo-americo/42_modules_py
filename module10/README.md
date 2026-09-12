# module10 — FuncMage: Master the Ancient Arts of Functional Programming

Material de estudo (TL;DR + aprofundamento por conceito): [`concept.md`](concept.md).

## Estrutura

O subject define cinco exercícios independentes, cada um com seu próprio
diretório e um único arquivo a submeter:

```
module10/
├── data_generator.py           # helper fornecido: dados de teste (mages, artifacts, spells)
├── ex0/
│   └── lambda_spells.py         # lambda + map/filter/sorted/min/max/sum
├── ex1/
│   └── higher_magic.py          # higher-order functions: função que recebe/retorna função
├── ex2/
│   └── scope_mysteries.py       # closures + escopo léxico (nonlocal)
├── ex3/
│   └── functools_artifacts.py   # functools: reduce, partial, lru_cache, singledispatch
└── ex4/
    └── decorator_mastery.py     # decoradores (com e sem parâmetros) + @staticmethod
```

Cada exercício sobe em dificuldade sobre o anterior: ex1 usa o conceito de
"função como valor" que o ex0 introduz de leve via lambda; ex2 aprofunda em
como uma função pode reter estado entre chamadas; ex3 usa esse mesmo padrão
já embutido em ferramentas prontas da biblioteca padrão; ex4 fecha o módulo
combinando tudo (função que envolve função) na forma de decorador.

## Partes do subject

| Exercício | Arquivo | Conceito principal |
|-----------|---------|---------------------|
| ex0 — Lambda Sanctum | `lambda_spells.py` | expressões `lambda` combinadas com `sorted`/`filter`/`map`/`max`/`min`/`sum` para transformação de dados sem `def` |
| ex1 — Higher Realm | `higher_magic.py` | funções de alta ordem: receber função como argumento e devolver uma função nova, preservando um contrato de assinatura fixo |
| ex2 — Memory Depths | `scope_mysteries.py` | closures e escopo léxico: uma função interna que "lembra" variáveis do escopo onde foi criada, usando `nonlocal` para reatribuir |
| ex3 — Ancient Library | `functools_artifacts.py` | `functools.reduce`/`partial`/`lru_cache`/`singledispatch` — ferramentas prontas que aplicam os padrões dos exercícios anteriores |
| ex4 — Master's Tower | `decorator_mastery.py` | decoradores simples e parametrizados (`functools.wraps`) + `@staticmethod` numa classe |

## Rodando

```bash
uv run python module10/ex0/lambda_spells.py
uv run python module10/ex1/higher_magic.py
uv run python module10/ex2/scope_mysteries.py
uv run python module10/ex3/functools_artifacts.py
uv run python module10/ex4/decorator_mastery.py
```

Cada arquivo tem um `main()` protegido por `if __name__ == "__main__":`, que
demonstra as funções exigidas pelo subject com dados de exemplo (o ex0 usa
`data_generator.py`, fornecido junto do subject, para gerar magos/artefatos
de teste).

```bash
uv run flake8 module10/ex0 module10/ex1 module10/ex2 module10/ex3 module10/ex4
uv run mypy module10/ex0 module10/ex1 module10/ex2 module10/ex3 module10/ex4
```

Os cinco exercícios ficam limpos em `flake8` e `mypy`. O subject exige
Python 3.10+; o ambiente foi testado em Python 3.13.2.
