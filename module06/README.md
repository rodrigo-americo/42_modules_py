# module06 — The Codex: Mastering Python's Import Mysteries

Material de estudo (TL;DR + aprofundamento por conceito): [`concept.md`](concept.md).

## Estrutura

Diferente dos módulos anteriores, este módulo não usa pastas `ex0/ex1/ex2`
— o subject define uma árvore fixa própria: um único pacote `alchemy/` e
uma série de scripts `ft_*.py` na raiz do módulo, cada um testando uma
forma diferente de import contra esse pacote.

```
module06/
├── elements.py                        # create_fire, create_water
├── alchemy/
│   ├── __init__.py                    # expõe parte da API do pacote
│   ├── elements.py                    # create_earth, create_air
│   ├── potions.py                     # healing_potion, strength_potion
│   ├── grimoire/
│   │   ├── __init__.py
│   │   ├── light_spellbook.py         # sem dependência circular
│   │   ├── light_validator.py
│   │   ├── dark_spellbook.py          # com dependência circular (proposital)
│   │   └── dark_validator.py
│   └── transmutation/
│       ├── __init__.py
│       └── recipes.py                 # absoluto + relativo no mesmo arquivo
├── ft_alembic_{0..5}.py               # Parte I
├── ft_distillation_{0,1}.py           # Parte II
├── ft_transmutation_{0,1,2}.py        # Parte III
└── ft_kaboom_{0,1}.py                 # Parte IV
```

## Partes do subject

| Parte | Scripts | Conceito principal |
|-------|---------|---------------------|
| I — Alembic | `ft_alembic_0` a `5` | `import x` vs `from x import y`, acesso direto a arquivo vs via pacote, exposição parcial pelo `__init__.py` |
| II — Distillation | `ft_distillation_0`, `1` | import aninhado (módulo de um pacote importando de outro módulo do mesmo pacote), alias de pacote (`import ... as nome`) |
| III — Transmutation | `ft_transmutation_0` a `2` | import absoluto e relativo combinados no mesmo arquivo |
| IV — Kaboom | `ft_kaboom_0`, `1` | quebrar dependência circular (light) vs sofrer dela de propósito (dark) |

## Rodando

```bash
uv run flake8 module06/         # lint em todo o módulo
uv run mypy module06/           # type check
uv run python module06/ft_alembic_0.py
uv run python module06/ft_kaboom_1.py    # este último termina com traceback — é esperado
```

`ft_alembic_4.py` e `ft_kaboom_1.py` terminam em exceção não capturada de
propósito — o próprio subject pede esse comportamento como prova de que a
restrição de acesso (Parte I) e a dependência circular (Parte IV) são reais,
não só teóricas. `ft_alembic_4.py` também deixa um erro de `mypy`
intencional na mesma linha, pelo mesmo motivo.
