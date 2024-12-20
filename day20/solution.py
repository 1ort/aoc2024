from collections import defaultdict
from typing import Iterable, NamedTuple, Self
from itertools import product


class Vec(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Self) -> Self:  # type: ignore
        return Vec(self.x + other.x, self.y + other.y)  # type: ignore

    def __sub__(self, other: Self) -> Self:  # type: ignore
        return Vec(self.x - other.x, self.y - other.y)  # type: ignore


def parse_map(inp: Iterable[str]) -> tuple[dict[Vec, bool], Vec, Vec, Vec]:
    walls = {}
    start = None
    end = None
    max_x = 0
    max_y = 0
    for y, row in enumerate(inp):
        max_y = y
        for x, char in enumerate(row):
            max_x = x
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

    return walls, Vec(max_x, max_y), start, end


def calculate_distances(
    bounds: Vec,
    walls: dict[Vec, bool],
    start: Vec,
    excluded_walls: tuple[Vec, ...],
    end: Vec | None = None,
):
    weights = {Vec(x, y): 0 for x in range(bounds.x + 1) for y in range(bounds.y + 1)}
    queue = {start}
    step = 0

    while queue:
        current_queue = queue
        queue = set()

        for loc in current_queue:
            for dir in (Vec(1, 0), Vec(-1, 0), Vec(0, 1), Vec(0, -1)):
                step_into = loc + dir
                if any(
                    (
                        step_into.x < 0,
                        step_into.y < 0,
                        step_into.x > bounds.x,
                        step_into.y > bounds.y,
                        step_into in walls and step_into not in excluded_walls,
                        weights.get(step_into),
                    )
                ):
                    continue

                weights[step_into] = step + 1
                if step_into == end:
                    return weights
                queue.add(step_into)
        step += 1
    return weights


def calculate_shortest_path(
    bounds: Vec,
    walls: dict[Vec, bool],
    start: Vec,
    end: Vec,
    excluded_walls: tuple[Vec, ...],
):
    weights = calculate_distances(bounds, walls, start, excluded_walls, end)

    return weights[end]


if __name__ == "__main__":
    results = defaultdict(int)
    with open("input.txt") as f:
        walls, bounds, start, end = parse_map(map(str.strip, f))
        distances = calculate_distances(bounds, walls, start, ())
        distances = {k: v for k, v in distances.items() if k not in walls}

    for a, b in product(distances.keys(), distances.keys()):
        if (
            a <= b
            or a - b not in (Vec(0, 2), Vec(2, 0))
            or abs(distances[a] - distances[b]) < 100
        ):
            continue
        rel_dist = abs(distances[a] - distances[b])

        reversed_walls = {
            Vec(x, y): True
            for x in range(bounds.x + 1)
            for y in range(bounds.y + 1)
            if Vec(x, y) not in walls and Vec(x, y) not in (a, b)
        }
        cheat_dist = calculate_shortest_path(bounds, reversed_walls, a, b, ())
        saved_seconds = rel_dist - cheat_dist
        if 1 < cheat_dist <= 2 and saved_seconds >= 100:
            results[saved_seconds] += 1
    print(
        *(f"{k}: {v}" for k, v in sorted(results.items(), key=lambda k: k[0])), sep="\n"
    )
    print(sum(results.values()))
