# module03 — Data Quest: Mastering Python Collections

Material de estudo (TL;DR + aprofundamento por conceito): [`concept.md`](concept.md).

## Exercícios

| Dir  | Função                      | Conceito principal                                          |
|------|------------------------------|---------------------------------------------------------------|
| ex0  | `ft_command_quest`           | `sys.argv` como lista, indexação e slicing                    |
| ex1  | `ft_score_analytics`         | lista construída por concatenação, `try`/`except` em lote     |
| ex2  | `ft_coordinate_system`       | tuplas imutáveis, parsing manual de string sem `split()`      |
| ex3  | `ft_achievement_tracker`     | `set`, união/interseção/diferença, `random.sample()`          |
| ex4  | `ft_inventory_system`        | `dict`, `dict.keys()`/`dict.update()`, parsing chave:valor    |
| ex5  | `ft_data_stream`             | generators (`yield`), `next()`, remoção via slice assignment  |
| ex6  | `ft_data_alchemist`          | list/dict comprehensions                                      |

Cada exercício é um arquivo independente (só ele é submetido) — por isso
funções auxiliares definidas num exercício (ex: `split_on_commas` do ex2)
são redeclaradas, com lógica adaptada, no arquivo que precisa de algo
parecido (ex4), não importadas entre pastas.

## Restrição de builtins por exercício

Cada exercício deste módulo define sua própria lista de funções/métodos
autorizados — bem mais restrita do que "tudo que o Python oferece". Isso é
proposital: o objetivo pedagógico é forçar o uso do mecanismo específico
sendo ensinado (parsing manual, `set` em vez de lista+loop, comprehension em
vez de loop) em vez de atalhos prontos que contornam o aprendizado. Ver
`concept.md` para a lista completa por exercício.

## Rodando

```bash
uv run flake8 module03/         # lint em todo o módulo
uv run mypy module03/           # type check
uv run python module03/ex0/ft_command_quest.py hello world 42
```

O `ex2` e o `ex5` pedem entrada interativa (`input()`), então rodar sem
argumentos vai parar esperando digitação no terminal.
