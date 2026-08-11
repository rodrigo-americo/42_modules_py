import random

book: list[str] = [
    "Dragon Tamer",
    "Iron Will",
    "Night Stalker",
    "Puzzle Master",
    "Gold Hoarder",
    "Marathoner",
    "Silent Blade",
    "Lucky Star",
    "Crafting Genius",
    "World Savior",
    "Master Explorer",
    "Collector Supreme",
    "Untouchable",
    "Boss Slayer",
    "Speed Runner",
    "Survivor",
]


def gen_player_achievements() -> set[str]:
    qtd = random.randint(len(book) // 3, 2 * len(book) // 3)
    return set(random.sample(book, qtd))


if __name__ == "__main__":
    print("=== Achievement Tracker System ===")
    alice = gen_player_achievements()
    bob = gen_player_achievements()
    carlos = gen_player_achievements()
    jose = gen_player_achievements()

    print(f"Player Alice: {alice}")
    print(f"Player Bob: {bob}")
    print(f"Player Carlos: {carlos}")
    print(f"Player Jose: {jose}")

    all_achievements = alice.union(bob, carlos, jose)
    print(f"All distinct achievements: {all_achievements}")

    common = alice.intersection(bob, carlos, jose)
    print(f"Common achievements: {common}")

    only_alice = alice.difference(bob.union(carlos, jose))
    only_bob = bob.difference(alice.union(carlos, jose))
    only_carlos = carlos.difference(alice.union(bob, jose))
    only_jose = jose.difference(alice.union(bob, carlos))
    print(f"Only Alice has: {only_alice}")
    print(f"Only Bob has: {only_bob}")
    print(f"Only Carlos has: {only_carlos}")
    print(f"Only Jose has: {only_jose}")

    print(f"Alice is missing: {all_achievements.difference(alice)}")
    print(f"Bob is missing: {all_achievements.difference(bob)}")
    print(f"Carlos is missing: {all_achievements.difference(carlos)}")
    print(f"Jose is missing: {all_achievements.difference(jose)}")
