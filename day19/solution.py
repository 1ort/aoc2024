from functools import cache
from typing import Iterable, assert_never


def parse_input(inp: Iterable[str]):
    inp = map(str.strip, inp)
    inp = iter(inp)

    raw_towels = next(inp)
    towels = raw_towels.split(",")
    towels = map(str.strip, towels)

    assert next(inp) == ""

    return tuple(towels), list(inp)


@cache
def is_pattern_possible(pattern: str, towels: tuple[str]):
    for towel in towels:
        if towel == pattern:
            return True

        if not pattern.startswith(towel):
            continue

        rest = pattern[len(towel) :]
        is_possible = is_pattern_possible(rest, towels)
        if is_possible:
            return True

    return False


@cache
def count_possible_ways(pattern: str, towels: tuple[str]):
    ways_count = 0
    for towel in towels:
        if towel == pattern:
            ways_count += 1
            continue

        if not pattern.startswith(towel):
            continue

        rest = pattern[len(towel) :]
        possible_ways = count_possible_ways(rest, towels)
        ways_count += possible_ways

    return ways_count


if __name__ == "__main__":
    with open("input.txt") as f:
        towels, patterns = parse_input(f)

    possible_count = 0
    for pattern in patterns:
        is_possible = count_possible_ways(pattern, towels)
        possible_count += is_possible
        print(pattern, is_possible)
    print(possible_count)
