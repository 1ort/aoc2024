from enum import Enum, auto
from functools import total_ordering
from typing import Iterable, NamedTuple, Self
import sys
import heapq


class Vec(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Self) -> Self:  # type: ignore
        return Vec(self.x + other.x, self.y + other.y)  # type: ignore


@total_ordering
class Direction(Enum):
    east = auto()
    south = auto()
    west = auto()
    north = auto()

    def __lt__(self, other):
        return self.value > other.value


def direction_to_vec(d: Direction) -> Vec:
    return {
        Direction.east: Vec(1, 0),
        Direction.west: Vec(-1, 0),
        Direction.south: Vec(0, 1),
        Direction.north: Vec(0, -1),
    }[d]


def rotate_left(d: Direction) -> Direction:
    return {
        Direction.east: Direction.north,
        Direction.west: Direction.south,
        Direction.south: Direction.east,
        Direction.north: Direction.west,
    }[d]


def rotate_right(d: Direction) -> Direction:
    return {
        Direction.east: Direction.south,
        Direction.west: Direction.north,
        Direction.south: Direction.west,
        Direction.north: Direction.east,
    }[d]


def parse_map(inp: Iterable[str]) -> tuple[dict[Vec, bool], Vec, Vec]:
    walls = {}
    start = None
    end = None
    for y, row in enumerate(inp):
        for x, char in enumerate(row):
            if char == "#":
                walls[Vec(x, y)] = True
            elif char == "E":
                end = Vec(x, y)
            elif char == "S":
                start = Vec(x, y)
            elif char != ".":
                raise RuntimeError(f"Unknown character in map on {Vec(x, y)}: {char}")
    if start is None:
        raise RuntimeError
    if end is None:
        raise RuntimeError

    return walls, start, end


def calculate_cheapest_path(
    walls: dict[Vec, bool],
    start: Vec,
    end: Vec,
):
    queue = [(0, start, Direction.east, [start])]
    seen = {}
    best = set()
    low = float("inf")

    while queue:
        score, loc, face, path = heapq.heappop(queue)
        if score > low:
            break
        if loc == end:
            if low > score:
                best.clear()
            low = score
            best = best | set(path)
        seen[loc, face] = score

        for dir in (face, rotate_left(face), rotate_right(face)):
            step_into = loc + direction_to_vec(dir)
            if step_into in walls:
                continue
            cost = 1001 if dir != face else 1
            if seen.get((step_into, dir), float("inf")) > score + cost:
                heapq.heappush(
                    queue, (score + cost, step_into, dir, path + [step_into])
                )
    return low, len(best)


if __name__ == "__main__":
    with open("input.txt") as f:
        map_, initial, target = parse_map((row.strip() for row in f))
        print(
            calculate_cheapest_path(
                map_,
                initial,
                target,
            )
        )
