# module01 — Code Cultivation: Object-Oriented Garden Systems

Material de estudo (TL;DR + aprofundamento por conceito): [`concept.md`](concept.md).

## Exercícios

| Dir  | Função                | Conceito principal                              |
|------|------------------------|--------------------------------------------------|
| ex0  | `ft_garden_intro`       | `if __name__ == "__main__":`                    |
| ex1  | `ft_garden_data`        | classe, atributos, `show()`                      |
| ex2  | `ft_plant_growth`       | métodos que alteram estado (`grow()`, `age()`)   |
| ex3  | `ft_plant_factory`      | construção + inicialização via `__init__`        |
| ex4  | `ft_garden_security`    | encapsulamento (`_protected`), getters/setters   |
| ex5  | `ft_plant_types`        | herança, `super()`                                |
| ex6  | `ft_garden_analytics`   | `staticmethod`, `classmethod`, nested class       |

Todos os exercícios a partir do ex1 usam classes (exigência do subject a
partir deste ponto do módulo). Cada arquivo inclui um bloco
`if __name__ == "__main__":` para teste manual — explicitamente permitido
pelo subject desde o ex0.

## Rodando

```bash
uv run flake8 module01/         # lint em todo o módulo
uv run mypy module01/           # type check (obrigatório em todos os exercícios)
uv run python module01/ex6/ft_garden_analytics.py   # executar um exercício
```
