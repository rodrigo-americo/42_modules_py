def count_days(days: int) -> None:
    if (days > 1):
        count_days(days - 1)
        print(f"Day {days}")
    else:
        print(f"Day {days}")


def ft_count_harvest_recursive() -> None:
    days = int(input("Days until harvest: "))
    count_days(days)
    print("Harvest time!")
