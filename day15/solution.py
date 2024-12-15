from typing import Iterable
from itertools import takewhile


def parse_input(
    inp: Iterable[str],
) -> tuple[dict[tuple[int, int], int], Iterable[str], tuple[int, int]]:
    inp = map(str.strip, inp)
    inp = iter(inp)

    map_part = list(takewhile(bool, inp))
    commands = "".join(inp)

    map_ = {}
    robot_pos = None

    for y, row in enumerate(map_part):
        for x, char in enumerate(row):
            if char == "#":
                map_[(x, y)] = 0
            elif row[x] == "O":
                map_[(x, y)] = 1
            elif row[x] == "@":
                robot_pos = (x, y)

    if not robot_pos:
        raise RuntimeError("cant parse robot_pos")

    return map_, commands, robot_pos


def update_map(
    m: dict[tuple[int, int], int], pos: tuple[int, int], command: str
) -> tuple[int, int]:
    x, y = pos
    if command == "^":
        move_vector = (0, -1)
    elif command == ">":
        move_vector = (1, 0)
    elif command == "v":
        move_vector = (0, 1)
    elif command == "<":
        move_vector = (-1, 0)
    else:
        raise RuntimeError("Unknown input", command)

    move_to = (x + move_vector[0], y + move_vector[1])
    space_to_check = move_to
    box_on_the_way = False
    while m.get(space_to_check) == 1:
        box_on_the_way = True
        space_to_check = (
            space_to_check[0] + move_vector[0],
            space_to_check[1] + move_vector[1],
        )

    if m.get(space_to_check) is None:
        if box_on_the_way:
            del m[move_to]
            m[space_to_check] = 1
        return move_to
    elif m.get(space_to_check) == 0:
        return pos
    else:
        raise RuntimeError("invalid data in map", m.get(space_to_check))


def render_map(map_: dict[tuple[int, int], int], pos: tuple[int, int]):
    chars = {0: "#", 1: "O", None: "."}

    for y in range(50):
        print(
            "".join(
                [chars[map_.get((x, y))] if (x, y) != pos else "@" for x in range(50)]
            )
        )


def calculate_box_coordinate(pos: tuple[int, int]) -> int:
    return pos[1] * 100 + pos[0]


def calculate_gps_sum(map_: dict[tuple[int, int], int]) -> int:
    return sum(calculate_box_coordinate(pos) for pos, tile in map_.items() if tile == 1)


if __name__ == "__main__":
    with open("input.txt") as f:
        map_, commands, robot_pos = parse_input(f.readlines())
        for command in commands:
            robot_pos = update_map(map_, robot_pos, command)
        render_map(map_, robot_pos)
        print(calculate_gps_sum(map_))
