from typing import Iterable, NamedTuple
from pprint import pprint


class Cord(NamedTuple):
    x: int
    y: int


Map = tuple[tuple[int]]


def parse_map(inp: Iterable[str]) -> Map:
    result = list()
    for line in map(str.strip, inp):
        result.append(map(int, line))

    result = tuple(zip(*result))
    return result


def get_neighbors(map_: Map, cord: Cord) -> set[Cord]:
    neigbors = set()

    if cord.x > 0:
        neigbors.add(Cord(cord.x - 1, cord.y))
    if cord.x < len(map_) - 1:
        neigbors.add(Cord(cord.x + 1, cord.y))
    if cord.y > 0:
        neigbors.add(Cord(cord.x, cord.y - 1))
    if cord.y < len(map_[0]) - 1:
        neigbors.add(Cord(cord.x, cord.y + 1))

    return neigbors


def find_peaks(map_: Map, pos: Cord) -> set[Cord]:
    current_height = map_[pos.x][pos.y]
    peaks = set()
    for neighbor in get_neighbors(map_, pos):
        height = map_[neighbor.x][neighbor.y]

        if height - current_height == 1:
            if height == 9:
                peaks.add(neighbor)
            else:
                peaks.update(find_peaks(map_, neighbor))
    return peaks


def count_trails(map_: Map, pos: Cord) -> int:
    current_height = map_[pos.x][pos.y]
    score = 0

    for neighbor in get_neighbors(map_, pos):
        height = map_[neighbor.x][neighbor.y]

        if height - current_height == 1:
            if height == 9:
                score += 1
            else:
                score += count_trails(map_, neighbor)
    return score


def process_trailheads(map_: Map) -> int:
    total_score = 0

    for x, row in enumerate(map_):
        for y, height in enumerate(row):
            if height == 0:
                score = len(find_peaks(map_, Cord(x, y)))
                print(f"{x}:{y} {score}")
                total_score += score

    return total_score


def process_trailheads_p2(map_: Map) -> int:
    total_score = 0

    for x, row in enumerate(map_):
        for y, height in enumerate(row):
            if height == 0:
                score = count_trails(map_, Cord(x, y))
                print(f"{x}:{y} {score}")
                total_score += score

    return total_score


if __name__ == "__main__":
    with open("input.txt") as f:
        map_ = parse_map(f)
        pprint(map_)
        print(process_trailheads_p2(map_))
