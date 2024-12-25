from itertools import takewhile, product
from typing import Iterable


def parse_locks_and_keys(f: Iterable[str]) -> tuple[list[list[int]], list[list[int]]]:
    keys = []
    locks = []

    f = iter(f)
    while True:
        a = list(takewhile(bool, f))
        if not a:
            break
        candidate = list(zip(*a))
        if candidate[0][0] == '#':
            locks.append(parse_lock(candidate))
        else:
            keys.append(parse_lock(map(lambda s: s[::-1], candidate)))

    return locks, keys


def parse_lock(lock: Iterable[str]) -> list[int]:
    return [x.count('#') - 1 for x in lock]


if __name__ == '__main__':
    with open('input.txt') as f:
        f = list(map(str.strip, f))

    res = 0
    locks, keys = parse_locks_and_keys(f)
    for lock, key in product(locks, keys):
        if all(lock_pin + key_pin <= 5 for lock_pin, key_pin in zip(lock, key)):
            res += 1

    print(res)
