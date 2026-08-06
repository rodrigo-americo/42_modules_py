def garden_operations(operation_number: int) -> None:
    if (operation_number == 0):
        int('abc')
    elif (operation_number == 1):
        2 / 0
    elif (operation_number == 2):
        open("/non/existent/file")
    elif (operation_number == 3):
        "ola" + 5
    else:
        return


def test_error_types() -> None:
    samples = [0, 1, 2, 3, 4]
    for raw in samples:
        print(f"Testing operation {raw}...")
        try:
            garden_operations(raw)
        except (
            ValueError,
            ZeroDivisionError,
            FileNotFoundError,
            TypeError,
        ) as err:
            name = err.__class__.__name__
            print(f"Caught {name}: {err}")
        else:
            print("Operation completed successfully")


if (__name__ == "__main__"):
    print("=== Garden Error Types Demo ===")
    test_error_types()
    print()
    print("All error types tested successfully!")
