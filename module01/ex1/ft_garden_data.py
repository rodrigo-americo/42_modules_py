class Plant:

    def __init__(self, name: str, height: int, age: int) -> None:
        self.name = name
        self.height = height
        self.age = age

    def show(self) -> None:
        print(f"{self.name.title()}: {self.height}cm, {self.age} days old")


if (__name__ == '__main__'):
    print("=== Garden Plant Registry ===")
    plant1 = Plant("Rose", 25, 30)
    plant1.show()
    plant2 = Plant("Sunflower", 80, 45)
    plant2.show()
    plant3 = Plant("Cactus", 15, 120)
    plant3.show()
