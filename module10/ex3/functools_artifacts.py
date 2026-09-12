from functools import reduce, partial, lru_cache, singledispatch
from typing import Any
import operator
from collections.abc import Callable


def spell_reducer(spells: list[int], operation: str) -> int:
    if len(spells) < 1:
        return 0
    if operation == "add":
        return reduce(operator.add, spells)
    elif operation == "multiply":
        return reduce(operator.mul, spells)
    elif operation == "max":
        return reduce(max, spells)
    elif operation == "min":
        return reduce(min, spells)
    else:
        raise ValueError(f"Unknown operation: {operation}")


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    spells: dict[str, Callable] = {
        "fire": partial(base_enchantment, power=50, element="fire"),
        "ice": partial(base_enchantment, power=50, element="ice"),
        "lightning": partial(
            base_enchantment, power=50, element="lightning"
        ),
    }
    return spells


@lru_cache
def memoized_fibonacci(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


@singledispatch
def cast(spell: Any) -> str:
    return "Unknown spell type"


@cast.register
def _(spell: int) -> str:
    return f"{spell} damage"


@cast.register
def _(spell: str) -> str:
    return spell


@cast.register
def _(spell: list) -> str:
    return f"{len(spell)} spells"


def spell_dispatcher() -> Callable[[Any], str]:
    return cast


def enchant(power: int, element: str, target: str) -> str:
    return f"{element.capitalize()} enchant of {power} on {target}"


def main() -> None:
    print("Testing spell reducer...")
    powers = [10, 20, 30, 40]
    print(f"Sum: {spell_reducer(powers, 'add')}")
    print(f"Product: {spell_reducer(powers, 'multiply')}")
    print(f"Max: {spell_reducer(powers, 'max')}")
    print()

    print("Testing partial enchanter...")
    enchants = partial_enchanter(enchant)
    print(enchants["fire"](target="Sword"))
    print(enchants["ice"](target="Shield"))
    print()

    print("Testing memoized fibonacci...")
    print(f"Fib(0): {memoized_fibonacci(0)}")
    print(f"Fib(1): {memoized_fibonacci(1)}")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")
    print(memoized_fibonacci.cache_info())
    print()

    print("Testing spell dispatcher...")
    dispatcher = spell_dispatcher()
    print(f"Damage spell: {dispatcher(42)}")
    print(f"Enchantment: {dispatcher('fireball')}")
    print(f"Multi-cast: {dispatcher([1, 2, 3])}")
    print(dispatcher(3.14))


if __name__ == "__main__":
    main()
