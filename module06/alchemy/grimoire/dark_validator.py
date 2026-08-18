from .dark_spellbook import dark_spell_allowed_ingredients


def validate_dark_ingredients(ingredients: str) -> str:
    allowed = dark_spell_allowed_ingredients()
    lowered = ingredients.lower()
    if any(item in lowered for item in allowed):
        return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
