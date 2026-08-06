class Plant:

    def __init__(
            self,
            name: str,
            height: float,
            age: int,
            grow: float
    ) -> None:
        self.name = name
        self.height = height
        self._age = age
        self.qtd_grow = grow

    def show(self) -> None:
        print(
            f"{self.name.title()}: {self.height:.1f}cm, "
            f"{self._age} days old"
        )

    def grow(self) -> None:
        self.height += self.qtd_grow

    def age(self) -> None:
        self._age += 1


if (__name__ == '__main__'):
    plant = Plant("Rose", 25, 30, 2.3)
    print("Day 1")
    plant.show()
    plant.grow()
    plant.age()
    print("Day 2")
    plant.show()
    plant.grow()
    plant.age()
    plant2 = Plant("Maria", 50, 50, 1.58)
    print("Day 3")
    plant2.show()
    plant2.grow()
    plant2.age()
    print("Day 4")
    plant2.show()
    plant2.grow()
    plant2.age()
