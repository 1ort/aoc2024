from collections.abc import Iterable
from typing import NamedTuple


class Cord(NamedTuple):
    x: int
    y: int


def get_neighbors(cord: Cord, bounds: Cord) -> set[Cord]:
    neigbors = set()

    if cord.x > 0:
        neigbors.add(Cord(cord.x - 1, cord.y))
    if cord.x < bounds.x:
        neigbors.add(Cord(cord.x + 1, cord.y))
    if cord.y > 0:
        neigbors.add(Cord(cord.x, cord.y - 1))
    if cord.y < bounds.y:
        neigbors.add(Cord(cord.x, cord.y + 1))

    return neigbors


def parse_map(inp: Iterable[str]) -> tuple[dict[Cord, str], Cord]:
    res = {}
    max_y: int = 0
    max_x: int = 0
    for y, row in enumerate(inp):
        max_y = y
        row = row.strip()
        for x, char in enumerate(row):
            max_x = x
            res[Cord(x, y)] = char
    return res, Cord(max_x, max_y)


def split_regions(_map: dict[Cord, str], map_bounds: Cord):
    regions: list[tuple[set[Cord], str, int]] = []
    has_regions: set[Cord] = set()
    regions_queue: set[Cord] = set([Cord(0, 0)])

    print(bounds)
    while regions_queue:
        start_position = regions_queue.pop()
        if start_position in has_regions:
            continue

        current_region_char = _map[start_position]
        current_region_queue: set[Cord] = set([start_position])
        current_region: set[Cord] = set()
        current_region_perimeter = 0

        while current_region_queue:
            current_position = current_region_queue.pop()
            current_region.add(current_position)
            has_regions.add(current_position)
            neighbors = get_neighbors(current_position, map_bounds)
            current_region_perimeter += 4 - len(neighbors)
            print(f"{current_position=} {neighbors=}")
            for neighbor in neighbors:
                if (
                    _map[neighbor] == current_region_char
                    and neighbor not in current_region
                    and neighbor not in current_region_queue
                ):
                    current_region_queue.add(neighbor)
                elif _map[neighbor] != current_region_char:
                    regions_queue.add(neighbor)
                    current_region_perimeter += 1
        regions.append((current_region, current_region_char, current_region_perimeter))

        print(
            f"{current_region_char=}\n{len(current_region)=}\n{current_region_perimeter}"
        )
        print(f"{current_region=}")
        print(f"{regions_queue=}")

    result = sum(region[2] * len(region[0]) for region in regions)
    return result


if __name__ == "__main__":
    with open("input.txt") as f:
        map_, bounds = parse_map(f)
        print(split_regions(map_, bounds))
