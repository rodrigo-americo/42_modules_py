from abc import ABC, abstractmethod

from .aqua import Aquabub, Torragon
from .base import Creature
from .flame import Flameling, Pyrodon


class CreatureFactory(ABC):

    @abstractmethod
    def create_base(self) -> Creature:
        ...

    @abstractmethod
    def create_evolved(self) -> Creature:
        ...


class FlameFactory(CreatureFactory):

    def create_base(self) -> Flameling:
        return Flameling("Flameling", "Fire")

    def create_evolved(self) -> Pyrodon:
        return Pyrodon("Pyrodon", "Fire/Flying")


class AquaFactory(CreatureFactory):

    def create_base(self) -> Aquabub:
        return Aquabub("Aquabub", "Water")

    def create_evolved(self) -> Torragon:
        return Torragon("Torragon", "Water")
