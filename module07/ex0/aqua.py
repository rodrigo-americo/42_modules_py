from .base import Creature


class Aquabub(Creature):

    def attack(self) -> str:
        return "Aquabub uses Water Gun!"


class Torragon(Creature):

    def attack(self) -> str:
        return "Torragon uses Hydro Pump!"
