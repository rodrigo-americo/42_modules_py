def input_temperature(temp_str: str) -> int:
    return int(temp_str)


def test_temperature() -> None:
    samples = ["25", "abc"]
    for raw in samples:
        print(f"Input data is '{raw}'")
        try:
            print(f"Temperature is now {input_temperature(raw)}°C")
        except Exception as err:
            print(f"Caught input_temperature error: {err}")


if (__name__ == "__main__"):
    print("=== Garden Temperature ===")
    test_temperature()
    print("All tests completed - program didn't crash!")
