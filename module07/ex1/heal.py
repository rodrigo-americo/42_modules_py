from abc import ABC, abstractmethod
from typing import Any

from ex0.base import Creature


class HealCapability(ABC):

    @abstractmethod
    def heal(self, target: Any) -> str:
        ...


class Sproutling(Creature, HealCapability):

    def heal(self, target: Any = None) -> str:
        if target is None:
            return f"{self.name} heals itself for a small amount"
        return f"{target.name} is healed by Sproutling's healing ability!"

    def attack(self) -> str:
        return f"{self.name} attacks with a vine whip!"


class Bloomora(Creature, HealCapability):

    def heal(self, target: Any = None) -> str:
        if target is None:
            return f"{self.name} heals itself and others for a large amount"
        return f"{target.name} is healed by Bloomora's rejuvenating bloom!"

    def attack(self) -> str:
        return f"{self.name} uses Petal Dance!"
