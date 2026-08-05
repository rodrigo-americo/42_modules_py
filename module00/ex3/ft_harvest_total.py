def ft_harvest_total() -> None:
    harvest: int = int(input("Day 1 harvest: "))
    harvest += int(input("Day 2 harvest: "))
    harvest += int(input("Day 3 harvest: "))
    print(f"Total harvest: {harvest}")
