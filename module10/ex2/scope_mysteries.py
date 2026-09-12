from typing import Any
from collections.abc import Callable


def mage_counter() -> Callable[[], int]:
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count
    return counter


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    total: int = initial_power

    def accumulator(power: int) -> int:
        nonlocal total
        total += power
        return total
    return accumulator


def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:
    power: str = enchantment_type

    def enchantment(item: str) -> str:
        return power + " " + item
    return enchantment


def memory_vault() -> dict[str, Callable]:
    vault: dict[str, Any] = {}

    def store(key: str, value: Any) -> None:
        vault[key] = value

    def recall(key: str) -> Any:
        if vault.get(key) is None:
            return "Memory not found"
        return vault.get(key)

    return {"store": store, "recall": recall}


def main() -> None:
    print("Testing mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")
    print(f"counter_b call 1: {counter_b()}")
    print()

    print("Testing spell accumulator...")
    accumulate = spell_accumulator(100)
    print(f"Base 100, add 20: {accumulate(20)}")
    print(f"Base 100, add 30: {accumulate(30)}")
    print()

    print("Testing enchantment factory...")
    flaming = enchantment_factory("Flaming")
    frozen = enchantment_factory("Frozen")
    print(flaming("Sword"))
    print(frozen("Shield"))
    print()

    print("Testing memory vault...")
    vault = memory_vault()
    vault["store"]("secret", 42)
    print("Store 'secret' = 42")
    print(f"Recall 'secret': {vault['recall']('secret')}")
    print(f"Recall 'unknown': {vault['recall']('unknown')}")


if __name__ == "__main__":
    main()
