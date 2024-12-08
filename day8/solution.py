from collections import defaultdict
from itertools import permutations
from typing import Iterable

Cord = tuple[int, int]


def parse_map(inp: Iterable[str]) -> tuple[dict[str, set[Cord]], Cord]:
    antennas: dict[str, set[Cord]] = defaultdict(set)
    lines = map(str.strip, inp)
    max_x, max_y = 0, 0

    for y, line in enumerate(lines):
        max_y = y
        max_x = len(line) - 1
        for x, char in enumerate(line):
            if char == ".":
                continue
            antennas[char].add((x, y))
    return antennas, (max_x, max_y)


def is_in_bounds(a: Cord, bounds: Cord) -> bool:
    return 0 <= a[0] <= bounds[0] and 0 <= a[1] <= bounds[1]


def process(inp: Iterable[str], p2: bool = False) -> int:
    antennas, bounds = parse_map(inp)
    antinodes: set[Cord] = set()
    for freq in antennas.values():
        for first, second in permutations(freq, 2):
            for t in range(max(bounds[0], bounds[1])) if p2 else range(1, 2):
                antinode = (
                    first[0] - ((second[0] - first[0]) * t),
                    first[1] - ((second[1] - first[1]) * t),
                )
                if is_in_bounds(antinode, bounds):
                    antinodes.add(antinode)

    # for y in range(bounds[1]+1):
    #     for x in range(bounds[0]+1):
    #         if (x, y) in antinodes:
    #             char = '#'
    #         else:
    #             char = '.'
    #         print(char, end="")
    #     print()

    return len(antinodes)


if __name__ == "__main__":
    with open("input.txt") as f:
        result = process(f, True)
        print(result)
