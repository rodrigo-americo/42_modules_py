from abc import ABC, abstractmethod

from ex0.base import Creature
from ex1.heal import HealCapability
from ex1.transform import TransformCapability


class InvalidStrategyError(Exception):

    def __init__(self, message: str = "Unknown Battle Strategy error") -> None:
        super().__init__(message)


class BattleStrategy(ABC):

    @abstractmethod
    def act(self, creature: Creature) -> str:
        ...

    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        ...


class NormalStrategy(BattleStrategy):

    def act(self, creature: Creature) -> str:
        if self.is_valid(creature):
            return creature.attack()
        raise InvalidStrategyError(
            f"Invalid Creature '{creature.name}' for this normal strategy"
        )

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, Creature)


class AggressiveStrategy(BattleStrategy):

    def act(self, creature: Creature) -> str:
        if isinstance(creature, TransformCapability):
            return "\n".join(
                [creature.transform(), creature.attack(), creature.revert()]
            )
        raise InvalidStrategyError(
            f"Invalid Creature '{creature.name}' for this aggressive strategy"
        )

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)


class DefensiveStrategy(BattleStrategy):

    def act(self, creature: Creature) -> str:
        if isinstance(creature, HealCapability):
            return "\n".join([creature.attack(), creature.heal()])
        raise InvalidStrategyError(
            f"Invalid Creature '{creature.name}' for this defensive strategy"
        )

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)
