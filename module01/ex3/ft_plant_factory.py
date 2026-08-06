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
    print("=== Plant Factory Output ===")
    print("Created: ", end="")
    Plant("Rose", 25, 30, 12).show()
    print("Created: ", end="")
    Plant("Maria", 23, 12, 1).show()
    print("Created: ", end="")
    Plant("Hoje", 20, 40, 3).show()
    print("Created: ", end="")
    Plant("Plumo", 11, 1, 1).show()
    print("Created: ", end="")
    Plant("Rose2", 5, 3, 6).show()
