from ex0.factory import CreatureFactory

from .heal import Sproutling, Bloomora
from .transform import Shiftling, Morphagon


class HealingCreatureFactory(CreatureFactory):

    def create_base(self) -> Sproutling:
        return Sproutling("Sproutling", "Grass")

    def create_evolved(self) -> Bloomora:
        return Bloomora("Bloomora", "Grass/Fairy")


class TransformCreatureFactory(CreatureFactory):

    def create_base(self) -> Shiftling:
        return Shiftling("Shiftling", "Normal")

    def create_evolved(self) -> Morphagon:
        return Morphagon("Morphagon", "Normal/Dragon")
