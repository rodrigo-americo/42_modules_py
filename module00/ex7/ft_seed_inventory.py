def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    final = seed_type.title().strip() + " seeds: "
    if (unit.lower().strip() == "packets"):
        final += f"{quantity} {unit} available"
    elif (unit.lower().strip() == "grams"):
        final += f"{quantity} {unit} total"
    elif (unit.lower().strip() == "area"):
        final += f"covers {quantity} square meters"
    else:
        print("Unknown unit type")
        return
    print(final)
