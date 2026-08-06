def input_temperature(temp_str: str) -> int:
    temp = int(temp_str)
    if (temp > 40):
        raise ValueError(f"{temp_str}°C is too hot for plants (max 40°C)")
    elif (temp < 0):
        raise ValueError(f"{temp_str}°C is too cold for plants (min 0°C)")
    return temp


def test_temperature() -> None:
    samples = ["25", "abc", "100", "-50"]
    for raw in samples:
        print(f"Input data is '{raw}'")
        try:
            print(f"Temperature is now {input_temperature(raw)}°C")
        except (ValueError, TypeError) as err:
            print(f"Caught input_temperature error: {err}")


if (__name__ == "__main__"):
    print("=== Garden Temperature Checker ===")
    test_temperature()
    print("All tests completed - program didn't crash!")
