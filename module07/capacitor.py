from ex0 import CreatureFactory
from ex0.base import Creature
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex1.heal import HealCapability
from ex1.transform import TransformCapability


def describe_and_attack(creature: Creature, label: str) -> None:
    print(f" {label}:")
    print(creature.describe())
    print(creature.attack())


def test_healing(factory: CreatureFactory) -> None:
    print("Testing Creature with healing capability")
    for label, creature in (
        ("base", factory.create_base()),
        ("evolved", factory.create_evolved()),
    ):
        describe_and_attack(creature, label)
        if isinstance(creature, HealCapability):
            print(creature.heal(None))
    print()


def test_transform(factory: CreatureFactory) -> None:
    print("Testing Creature with transform capability")
    for label, creature in (
        ("base", factory.create_base()),
        ("evolved", factory.create_evolved()),
    ):
        describe_and_attack(creature, label)
        if isinstance(creature, TransformCapability):
            print(creature.transform())
            print(creature.attack())
            print(creature.revert())
    print()


def main() -> None:
    try:
        test_healing(HealingCreatureFactory())
        test_transform(TransformCreatureFactory())
    except Exception as error:
        print(f"capacitor error: {error}")


if __name__ == "__main__":
    main()
