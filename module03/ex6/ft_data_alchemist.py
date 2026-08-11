import random

players: list[str] = [
    "Nadia", "theo", "Winston", "rin", "Farid", "Beatrix", "milo", "quinn",
]

if __name__ == "__main__":
    print("=== Game Data Alchemist ===")
    print(f"Initial list of players: {players}")

    players_capitalized = [name.capitalize() for name in players]
    print(f"New list with all names capitalized: {players_capitalized}")

    players_is_capitalized = [
        name for name in players if name.capitalize() == name
    ]
    print(f"New list of capitalized names only: {players_is_capitalized}")

    players_value = {
        name: random.randint(1, 100) for name in players_capitalized
    }
    print(f"Score dict: {players_value}")

    mean = sum(
        [players_value[name] for name in players_capitalized]
    ) / len(players_capitalized)
    print(f"Score average is {round(mean, 2)}")

    players_greater_mean = {
        name: players_value[name]
        for name in players_capitalized
        if players_value[name] > mean
    }
    print(f"High scores: {players_greater_mean}")
