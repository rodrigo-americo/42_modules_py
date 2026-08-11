import math


def split_on_commas(text: str) -> list[str]:
    fields: list[str] = []
    tmp: str = ""
    for c in text:
        if c == ',':
            fields += [tmp]
            tmp = ""
        else:
            tmp += c
    fields += [tmp]
    return fields


def fields_to_floats(fields: list[str]) -> list[float]:
    values: list[float] = []
    for i in fields:
        try:
            values += [float(i)]
        except ValueError as err:
            print(f"Error on parameter '{i}': {str(err)}")
    return values


def get_player_pos() -> tuple[float, float, float]:
    while True:
        pos_str = input("Enter new coordinates as floats in format 'x,y,z':")
        pos_tmp = split_on_commas(pos_str)
        if len(pos_tmp) != 3:
            print("Invalid syntax")
            continue
        pos_float = fields_to_floats(pos_tmp)
        if len(pos_float) == 3:
            break
    return (pos_float[0], pos_float[1], pos_float[2])


def calc_distance(
    point1: tuple[float, float, float],
    point2: tuple[float, float, float],
) -> float:
    return math.sqrt(
        (point1[0] - point2[0]) ** 2
        + (point1[1] - point2[1]) ** 2
        + (point1[2] - point2[2]) ** 2
    )


if __name__ == "__main__":
    print("=== Game Coordinate System ===")
    p1: tuple[float, float, float] = get_player_pos()
    print(f"Got a first tuple: {p1}")
    print(f"It includes: X={p1[0]}, Y={p1[1]}, Z={p1[2]}")
    print(
        "Distance to center: "
        f"{round(calc_distance(p1, (0.0, 0.0, 0.0)), 4)}"
    )
    p2: tuple[float, float, float] = get_player_pos()
    print(f"Got a second tuple: {p2}")
    print(f"It includes: X={p2[0]}, Y={p2[1]}, Z={p2[2]}")
    distance = round(calc_distance(p2, p1), 4)
    print(f"Distance between the 2 sets of coordinates: {distance}")
