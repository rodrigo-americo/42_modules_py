from ex0 import AquaFactory, CreatureFactory, FlameFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    AggressiveStrategy,
    BattleStrategy,
    DefensiveStrategy,
    InvalidStrategyError,
    NormalStrategy,
)

Opponent = tuple[CreatureFactory, BattleStrategy]


def battle(opponents: list[Opponent]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    for i, (factory_a, strategy_a) in enumerate(opponents):
        for factory_b, strategy_b in opponents[i + 1:]:
            creature_a = factory_a.create_base()
            creature_b = factory_b.create_base()
            print()
            print("* Battle *")
            print(creature_a.describe())
            print("vs.")
            print(creature_b.describe())
            print("now fight!")
            try:
                print(strategy_a.act(creature_a))
                print(strategy_b.act(creature_b))
            except InvalidStrategyError as error:
                print(f"Battle error, aborting tournament: {error}")
                return


def main() -> None:
    flame_factory = FlameFactory()
    healing_factory = HealingCreatureFactory()
    transform_factory = TransformCreatureFactory()

    normal = NormalStrategy()
    aggressive = AggressiveStrategy()
    defensive = DefensiveStrategy()

    print("Tournament 0 (basic)")
    battle([(flame_factory, normal), (healing_factory, defensive)])

    print()
    print("Tournament 1 (error)")
    battle([(flame_factory, aggressive), (healing_factory, defensive)])

    print()
    print("Tournament 2 (multiple)")
    battle(
        [
            (AquaFactory(), normal),
            (healing_factory, defensive),
            (transform_factory, aggressive),
        ]
    )


if __name__ == "__main__":
    main()
