# module00 — Growing Code

Python Fundamentals Through Garden Data.

Material de estudo (TL;DR + aprofundamento por conceito): [`concept.md`](concept.md).

## Exercícios

| Dir  | Função                                                          | Conceito principal            |
|------|------------------------------------------------------------------|--------------------------------|
| ex0  | `ft_hello_garden`                                                | `print()` básico               |
| ex1  | `ft_garden_name`                                                 | `input()` + f-string           |
| ex2  | `ft_plot_area`                                                   | conversão de tipo (`int()`)    |
| ex3  | `ft_harvest_total`                                               | acumulador                     |
| ex4  | `ft_plant_age`                                                   | `if`/`else`                    |
| ex5  | `ft_water_reminder`                                              | `if`/`else`                    |
| ex6  | `ft_count_harvest_iterative`, `ft_count_harvest_recursive`       | iteração vs. recursão          |
| ex7  | `ft_seed_inventory`                                              | type hints obrigatórios        |

Cada exercício é um arquivo próprio contendo **só** a função pedida — sem
`if __name__ == "__main__":`, sem chamada direta, sem código fora de função
(exigência explícita do subject).

## Rodando

```bash
uv run flake8 module00/         # lint em todo o módulo
uv run mypy module00/ex7/       # type check (obrigatório a partir do ex7)
```
