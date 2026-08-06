class Plant:

    def __init__(
            self,
            name: str = "Rose",
            height: float = 1,
            age: int = 1,
            grow: float = 0.1
    ) -> None:
        self._name = name
        if (height <= 0):
            print("Invalid value for height starting with a value of 1.")
            self.set_height(1, verbose=False)
        else:
            self.set_height(height, verbose=False)
        if (age <= 0):
            print("Invalid value for age starting with a value of 1.")
            self.set_age(1, verbose=False)
        else:
            self.set_age(age, verbose=False)
        self._qtd_grow = grow

    def set_age(self, age: int, verbose: bool = True) -> None:
        if age <= 0:
            print("Invalid value for ages must be greater than 0.")
            return
        self._age = age
        if verbose:
            print(f"Age updated: {self.get_age()} days")

    def get_age(self) -> int:
        return self._age

    def set_height(self, height: float, verbose: bool = True) -> None:
        if height <= 0:
            print("Invalid value for height must be greater than 0.")
            return
        self._height = height
        if verbose:
            print(f"Height updated: {self.get_height()} cm")

    def get_height(self) -> float:
        return self._height

    def show(self) -> None:
        print(
            f"{self._name.title()}: {self.get_height():.1f}cm, "
            f"{self.get_age()} days old"
        )

    def grow(self) -> None:
        self.set_height(self.get_height() + self._qtd_grow)

    def age(self) -> None:
        self.set_age(self.get_age() + 1)


class Flower(Plant):
    _is_bloom: bool = False

    def __init__(
            self,
            name: str = "Rose",
            height: float = 1,
            age: int = 1,
            grow: float = 0.1,
            color: str = "Red"
    ) -> None:
        super().__init__(name, height, age, grow)
        self._color = color

    def show(self) -> None:
        super().show()
        print(f"color: {self._color}, Is bloom: {self._is_bloom}")

    def bloom(self) -> None:
        self._is_bloom = True
        print(f"Is time to {self._name} bloom")


class Tree(Plant):

    def __init__(
            self,
            name: str = "Oukwe",
            height: float = 1,
            age: int = 1,
            grow: float = 0.1,
            trunk_diameter: float = 1
    ) -> None:
        super().__init__(name, height, age, grow)
        self._trunk_diameter = trunk_diameter

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {self._trunk_diameter:.1f}cm")

    def produce_shade(self) -> None:
        print("It casts a shadow that is disproportionate to the tree.")


class Vegetable(Plant):

    def __init__(
            self,
            name: str = "Rose",
            height: float = 1,
            age: int = 1,
            grow: float = 0.1,
            harvest_season: str = "Summer",
            nutritional_value: float = 1
    ) -> None:
        super().__init__(name, height, age, grow)
        self._nutritional_value = nutritional_value
        self._harvest_season = harvest_season

    def show(self) -> None:
        super().show()
        print(
            f"Harvest season: {self._harvest_season}, "
            f"Nutritional value: {self._nutritional_value}"
        )


if (__name__ == '__main__'):
    print("=== Garden Plant Types ===")

    print("=== Flower")
    rose = Flower("Rose", 15, 10, 8, "red")
    rose.show()
    print("[asking the rose to bloom]")
    rose.bloom()
    rose.show()

    print("=== Tree")
    oak = Tree("Oak", 200, 365, 5, 5)
    oak.show()
    print("[asking the oak to produce shade]")
    oak.produce_shade()

    print("=== Vegetable")
    tomato = Vegetable("Tomato", 5, 10, 2, "April", 0)
    tomato.show()
