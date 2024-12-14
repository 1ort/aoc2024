from functools import reduce
from typing import Iterable, NamedTuple
from pprint import pprint


class Vec2(NamedTuple):
    x: int
    y: int


class Robot(NamedTuple):
    pos: Vec2
    vel: Vec2


W, H = 101, 103


def parse_robot(r: str):
    pos_raw, velocity_raw = r.split(" ")

    pos = map(int, pos_raw.split("=")[1].split(","))
    velocity = map(int, velocity_raw.split("=")[1].split(","))

    return Robot(Vec2(*pos), Vec2(*velocity))


def simulate_seconds(r: Robot, n: int) -> Robot:
    new_pos = Vec2(
        (r.pos.x + (r.vel.x * n)) % W,
        (r.pos.y + (r.vel.y * n)) % H,
    )
    return Robot(new_pos, r.vel)


def calculate_safety_factor(robots: Iterable[Robot]) -> int:
    quadrants = {(1, 0): 0, (1, 1): 0, (0, 0): 0, (0, 1): 0}

    midW = W // 2
    midH = H // 2

    for r in robots:
        if r.pos.x == midW or r.pos.y == midH:
            continue
        xq = r.pos.x < midW
        yq = r.pos.y < midH

        quadrants[(int(xq), int(yq))] += 1
    return reduce(int.__mul__, quadrants.values(), 1)


def render_robots(robots: Iterable[Robot]):
    d = {r.pos: 1 for r in robots}

    print(
        "\n".join(
            "".join("#" if Vec2(x, y) in d else "." for x in range(W)) for y in range(H)
        )
    )


def count_surrounded(robots: Iterable[Robot]):
    d = {r.pos: 1 for r in robots}

    res = 0

    for pos in d:
        x = pos.x
        y = pos.y
        if all(
            (
                neigh in d
                for neigh in (
                    Vec2(x - 1, y - 1),
                    Vec2(x, y - 1),
                    Vec2(x + 1, y - 1),
                    Vec2(x - 1, y),
                    Vec2(x + 1, y),
                    Vec2(x - 1, y + 1),
                    Vec2(x, y + 1),
                    Vec2(x + 1, y + 1),
                )
            )
        ):
            res += 1
    return res


def find_largest_cluster_timing(robots: list[Robot], limit: int):
    surrounded_robots = []
    for i in range(limit):
        r = map(lambda robot: simulate_seconds(robot, i), robots)
        surrounded_ = count_surrounded(r)
        surrounded_robots.append(surrounded_)
    max_surr = max(surrounded_robots)
    return surrounded_robots.index(max_surr)


if __name__ == "__main__":
    with open("input.txt") as f:
        robots = list(map(parse_robot, f.readlines()))

        largest_cluster_second = find_largest_cluster_timing(robots, 10000)

        print(
            render_robots(
                map(
                    lambda robot: simulate_seconds(robot, largest_cluster_second),
                    robots,
                )
            )
        )
        print(largest_cluster_second)
