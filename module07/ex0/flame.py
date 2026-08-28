from .base import Creature


class Flameling(Creature):

    def attack(self) -> str:
        return "Flameling uses Ember!"


class Pyrodon(Creature):

    def attack(self) -> str:
        return "Pyrodon uses Flamethrower!"
