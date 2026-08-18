def validate_ingredients(ingredients: str, allowed: list[str]) -> str:
    lowered = ingredients.lower()
    if any(item in lowered for item in allowed):
        return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
