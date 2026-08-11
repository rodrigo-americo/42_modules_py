import sys


def ft_split(text: str) -> tuple[str, str]:
    key: str = ""
    value: str = ""
    tmp: str = ""
    qtd_twopoints = 0
    for c in text:
        if c == ':':
            qtd_twopoints += 1
            key = tmp
            tmp = ""
        else:
            tmp += c
    value = tmp
    if qtd_twopoints != 1:
        raise ValueError(f"Error - invalid parameter '{text}'")
    return (key, value)


def fields_to_int(fields: dict[str, str]) -> dict[str, int]:
    result: dict[str, int] = {}
    for key in fields.keys():
        try:
            result.update({key: int(fields[key])})
        except ValueError as err:
            print(f"Error on parameter '{key}': {str(err)}")
    return result


def creat_inventory(itens: list[str]) -> dict[str, int]:
    inventory: dict[str, str] = {}
    for item in itens:
        try:
            key, value = ft_split(item)
            if key in inventory:
                raise ValueError(f"Redundant item '{key}' - discarding")
            inventory.update({key: value})
        except ValueError as err:
            print(str(err))

    return fields_to_int(inventory)


def print_abundant(inventory: dict[str, int]) -> None:
    most = ""
    least = ""
    for item in inventory.keys():
        if most == "" and least == "":
            most = item
            least = item
        else:
            if (inventory[most] < inventory[item]):
                most = item
            if (inventory[least] > inventory[item]):
                least = item
    print(f"Item most abundant: {most} with quantity {inventory[most]}")
    print(f"Item least abundant: {least} with quantity {inventory[least]}")


if __name__ == "__main__":
    print("=== Inventory System Analysis ===")
    inventory = creat_inventory(sys.argv[1:])
    total_qtd = sum(inventory.values())
    if total_qtd == 0:
        print("empty inventory")
    else:
        print(f"Got inventory {inventory}")
        print(f"Item list: {list(inventory.keys())}")
        item_count = len(inventory.values())
        print(f"Total quantity of the {item_count} items: {total_qtd}")
        for item in inventory.keys():
            percent = round(inventory[item] / total_qtd * 100, 1)
            print(f"Item {item} represents {percent}%")
        print_abundant(inventory)
        inventory.update({"relic": 1})
        print(f"Updated inventory: {inventory}")
