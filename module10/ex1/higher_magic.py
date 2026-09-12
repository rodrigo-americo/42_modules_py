from collections.abc import Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined(target: str, power: int) -> tuple:
        return (spell1(target, power), spell2(target, power))
    return combined


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplifier(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplifier


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def cast(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return cast


def spell_sequence(spells: list[Callable]) -> Callable:
    def mult_cast(target: str, power: int) -> list[str]:
        result: list[str] = []
        for spell in spells:
            result.append(spell(target, power))
        return result
    return mult_cast


def zap(target: str, power: int) -> str:
    return f"Zap shocks {target} for {power} damage"


def mend(target: str, power: int) -> str:
    return f"Mend restores {target} for {power} HP"


def main() -> None:
    print("Testing spell combiner...")
    combined = spell_combiner(zap, mend)
    print(f"Combined spell result: {combined('Golem', 15)}")
    print()

    print("Testing power amplifier...")
    mega_zap = power_amplifier(zap, 3)
    print(f"Original: {zap('Golem', 10)}")
    print(f"Amplified: {mega_zap('Golem', 10)}")
    print()

    print("Testing conditional caster...")
    guarded = conditional_caster(lambda target, power: power >= 20, zap)
    print(f"Enough power: {guarded('Golem', 25)}")
    print(f"Not enough power: {guarded('Golem', 5)}")
    print()

    print("Testing spell sequence...")
    sequence = spell_sequence([zap, mend])
    print(f"Sequence result: {sequence('Golem', 12)}")


if __name__ == "__main__":
    main()
