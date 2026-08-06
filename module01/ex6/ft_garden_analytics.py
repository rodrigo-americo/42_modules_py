class Plant:

    class _Stats:
        def __init__(self) -> None:
            self._grow_calls = 0
            self._age_calls = 0
            self._show_calls = 0

        def show(self) -> None:
            print(
                f"Stats: {self.get_grow_call()} grow, "
                f"{self.get_age_call()} age, "
                f"{self.get_show_call()} show"
            )

        def registrar_grow(self) -> None:
            self._grow_calls += 1

        def get_grow_call(self) -> int:
            return self._grow_calls

        def registrar_age(self) -> None:
            self._age_calls += 1

        def get_age_call(self) -> int:
            return self._age_calls

        def registrar_show(self) -> None:
            self._show_calls += 1

        def get_show_call(self) -> int:
            return self._show_calls

    class _TreeStats(_Stats):
        def __init__(self) -> None:
            super().__init__()
            self._shade_calls = 0

        def show(self) -> None:
            super().show()
            print(f"{self.get_shade_call()} shade")

        def registrar_shade(self) -> None:
            self._shade_calls += 1

        def get_shade_call(self) -> int:
            return self._shade_calls

    @classmethod
    def anonymous(cls) -> "Plant":
        return cls("Unknown")

    def __init__(
            self,
            name: str = "Rose",
            height: float = 1,
            age: int = 1,
            grow: float = 0.1
    ) -> None:
        self._stats: Plant._Stats = Plant._Stats()
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
        self._stats.registrar_show()
        print(
            f"{self._name.title()}: {self.get_height():.1f}cm, "
            f"{self.get_age()} days old"
        )

    def grow(self) -> None:
        self._stats.registrar_grow()
        self.set_height(self.get_height() + self._qtd_grow)

    def age(self) -> None:
        self._stats.registrar_age()
        self.set_age(self.get_age() + 1)

    @staticmethod
    def is_been_at_least_year(qtd_days: int) -> bool:
        return qtd_days > 365


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


class Seed(Flower):

    def __init__(
            self,
            name: str = "Rose",
            height: float = 1,
            age: int = 1,
            grow: float = 0.1,
            color: str = "Red"
    ) -> None:
        super().__init__(name, height, age, grow, color)
        self._qtd_seed = 0

    def show(self) -> None:
        super().show()
        print(f"Qtd seeds: {self.get_qtd_seeds()}")

    def set_qtd_seeds(self, qtd: int) -> None:
        if (self._is_bloom):
            self._qtd_seed = qtd
        else:
            print("The flower hasn't bloomed yet.")

    def get_qtd_seeds(self) -> int:
        return self._qtd_seed


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
        self._stats: Plant._TreeStats = Plant._TreeStats()
        self._trunk_diameter = trunk_diameter

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {self._trunk_diameter:.1f}cm")

    def produce_shade(self) -> None:
        self._stats.registrar_shade()
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


def show_stasts_plats(plant: Plant) -> None:
    plant._stats.show()


if (__name__ == '__main__'):
    print("=== Garden statistics ===")

    print("=== Check year-old")
    is_30_old = Plant.is_been_at_least_year(30)
    print(f"Is 30 days more than a year? -> {is_30_old}")
    is_400_old = Plant.is_been_at_least_year(400)
    print(f"Is 400 days more than a year? -> {is_400_old}")

    print("=== Flower")
    rose = Flower("Rose", 15, 10, 8, "red")
    rose.show()
    show_stasts_plats(rose)
    print("[asking the rose to grow and bloom]")
    rose.grow()
    rose.bloom()
    rose.show()
    show_stasts_plats(rose)

    print("=== Tree")
    oak = Tree("Oak", 200, 365, 5, 5)
    oak.show()
    show_stasts_plats(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    oak.show()
    show_stasts_plats(oak)

    print("=== Seed")
    sunflower = Seed("Sunflower", 80, 45, 15, "yellow")
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    sunflower.grow()
    sunflower.age()
    sunflower.bloom()
    sunflower.set_qtd_seeds(42)
    sunflower.show()
    show_stasts_plats(sunflower)

    print("=== Anonymous")
    unknown = Plant.anonymous()
    unknown.show()
    show_stasts_plats(unknown)
