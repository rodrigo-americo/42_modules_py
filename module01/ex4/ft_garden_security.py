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


if (__name__ == '__main__'):
    print("=== Garden Security System ===")
    p = Plant("Rose", 25, 30, 12)
    p.show()
    p.set_height(35)
    p.set_age(10)
    p.set_height(-5)
    p.set_age(-9)
    print("Current state: ", end='')
    p.show()
