from ex0 import AquaFactory, CreatureFactory, FlameFactory


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    base = factory.create_base()
    evolved = factory.create_evolved()
    for creature in (base, evolved):
        print(creature.describe())
        print(creature.attack())
    print()


def test_battle(
    factory_a: CreatureFactory, factory_b: CreatureFactory
) -> None:
    print("Testing battle")
    creature_a = factory_a.create_base()
    creature_b = factory_b.create_base()
    print(creature_a.describe())
    print("vs.")
    print(creature_b.describe())
    print("fight!")
    print(creature_a.attack())
    print(creature_b.attack())


def main() -> None:
    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()

    test_factory(flame_factory)
    test_factory(aqua_factory)
    test_battle(flame_factory, aqua_factory)


if __name__ == "__main__":
    main()
