import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from data_generator import FuncMageDataGenerator  # noqa: E402


def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda art: art["power"], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda mage: mage["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: "* " + spell + " *", spells))


def mage_stats(mages: list[dict]) -> dict:
    max_power = max(mages, key=lambda mage: mage["power"])["power"]
    min_power = min(mages, key=lambda mage: mage["power"])["power"]
    avg_power = round(
        sum(map(lambda mage: mage["power"], mages)) / len(mages), 2
    )
    return {
        "max_power": max_power,
        "min_power": min_power,
        "avg_power": avg_power,
    }


def main() -> None:
    artifacts = FuncMageDataGenerator.generate_artifacts(4)
    mages = FuncMageDataGenerator.generate_mages(5)
    spells = FuncMageDataGenerator.generate_spells(4)

    print("Testing artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts)
    first, second = sorted_artifacts[0], sorted_artifacts[1]
    print(
        f"{first['name']} ({first['power']} power) comes before "
        f"{second['name']} ({second['power']} power)"
    )
    print()

    print("Testing power filter...")
    filtered = power_filter(mages, min_power=70)
    print(f"Mages with power >= 70: {[m['name'] for m in filtered]}")
    print()

    print("Testing spell transformer...")
    print(" ".join(spell_transformer(spells)))
    print()

    print("Testing mage stats...")
    print(mage_stats(mages))


if __name__ == "__main__":
    main()
