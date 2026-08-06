# module02 — Garden Guardian: Data Engineering for Smart Agriculture

Subject original em `py2.pdf` (não versionado — ver `.gitignore` na raiz).

Material de estudo (TL;DR + aprofundamento por conceito): [`concept.md`](concept.md).

## Exercícios

| Dir  | Função                  | Conceito principal                                    |
|------|--------------------------|--------------------------------------------------------|
| ex0  | `ft_first_exception`     | `try`/`except`, programa não crasha                     |
| ex1  | `ft_raise_exception`     | `raise` explícito, validação de faixa de valores        |
| ex2  | `ft_different_errors`    | múltiplos tipos de exceção num único `try`              |
| ex3  | `ft_custom_errors`       | exceções customizadas, hierarquia de herança            |
| ex4  | `ft_finally_block`       | `finally`, ordem de execução com `return` dentro do `except` |

Cada exercício é um arquivo independente (só ele é submetido) — por isso
classes definidas num exercício anterior (ex: `PlantError` do ex3) são
redeclaradas no arquivo que as usa (ex4), não importadas entre pastas.

## Rodando

```bash
uv run flake8 module02/         # lint em todo o módulo
uv run mypy module02/           # type check
uv run python module02/ex4/ft_finally_block.py   # executar um exercício
```

O `mypy` acusa um erro **intencional** em `ex2/ft_different_errors.py`
(operação que soma `str` + `int`) — o próprio subject avisa que isso é
esperado, porque o objetivo daquele trecho é gerar um `TypeError` real em
tempo de execução para o exercício capturar.
