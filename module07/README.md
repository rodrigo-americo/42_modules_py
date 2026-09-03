# module07 — DataDeck: Abstract Card Architecture

Material de estudo (TL;DR + aprofundamento por conceito): [`concept.md`](concept.md).

## Estrutura

O subject não desenha uma árvore de arquivos explícita, só descreve o que
cada pacote de exercício (`ex0/`, `ex1/`, `ex2/`) deve expor. Dentro de cada
pacote, os arquivos foram divididos por responsabilidade (classe abstrata,
famílias concretas, fábricas) em vez de um único arquivo — separação livre,
não exigida literalmente pelo subject.

```
module07/
├── battle.py                  # testa ex0 (abstract factory)
├── capacitor.py                # testa ex1 (capabilities), construído sobre ex0
├── tournament.py                # testa ex2 (abstract strategy), construído sobre ex0 + ex1
├── ex0/
│   ├── __init__.py             # expõe só as factories, nunca as Creature concretas
│   ├── base.py                 # Creature (ABC): attack abstrato, describe concreto
│   ├── flame.py                # família Flame: base + evoluída
│   ├── aqua.py                 # família Aqua: base + evoluída
│   └── factory.py              # CreatureFactory (ABC) + 2 factories concretas
├── ex1/
│   ├── __init__.py             # expõe só as factories de capability
│   ├── heal.py                 # HealCapability (ABC) + família com cura
│   ├── transform.py             # TransformCapability (ABC) + família com transformação
│   └── factory.py              # 2 factories concretas, reaproveitando CreatureFactory
└── ex2/
    ├── __init__.py              # expõe strategies + exceção dedicada
    └── BattleStrategy.py         # BattleStrategy (ABC) + 3 strategies concretas
```

## Partes do subject

| Exercício | Script raiz | Conceito principal |
|-----------|-------------|---------------------|
| ex0 — Creature Factory | `battle.py` | *abstract factory*: uma fábrica abstrata cria pares (base + evoluída) de uma família, sem o cliente conhecer as classes concretas |
| ex1 — Capabilities | `capacitor.py` | mixins de capacidade via herança múltipla, deliberadamente **não** ligados a `Creature` na base, para permitir reuso fora do domínio de criaturas |
| ex2 — Abstract Strategy | `tournament.py` | *strategy pattern*: o comportamento de batalha (`act`) varia por estratégia, e cada estratégia decide sozinha (`is_valid`) se é compatível com a criatura recebida |

## Rodando

```bash
uv run flake8 module07/         # lint em todo o módulo
uv run mypy module07/           # type check
uv run python module07/battle.py
uv run python module07/capacitor.py
uv run python module07/tournament.py
```
