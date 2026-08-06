class GardenError(Exception):

    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message: str = "Unknown water error") -> None:
        super().__init__(message)


def test_plant_error() -> None:
    print("Testing PlantError...")
    try:
        raise PlantError("The tomato plant is wilting!")
    except PlantError as err:
        print(f"Caught PlantError: {err}")


def test_water_error() -> None:
    print("Testing WaterError...")
    try:
        raise WaterError("Not enough water in the tank!")
    except WaterError as err:
        print(f"Caught WaterError: {err}")


def test_garden_error() -> None:
    print("Testing catching all garden errors...")
    for err_to_raise in (
        PlantError("The tomato plant is wilting!"),
        WaterError("Not enough water in the tank!"),
    ):
        try:
            raise err_to_raise
        except GardenError as err:
            print(f"Caught GardenError: {err}")


if (__name__ == "__main__"):
    print("=== Custom Garden Errors Demo ===")
    test_plant_error()
    print()
    test_water_error()
    print()
    test_garden_error()
    print()
    print("All custom error types work correctly!")
