from typing import Iterable, NamedTuple, Self


class Vec(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Self) -> Self:  # type: ignore
        return Vec(self.x + other.x, self.y + other.y)  # type: ignore


def parse_map(inp: Iterable[str], limit: int) -> dict[Vec, bool]:
    limited = (x for x, _ in zip(inp, range(limit)))
    return {Vec(*map(int, byte.split(","))): True for byte in limited}


def calculate_cheapest_path(
    bounds: Vec,
    walls: dict[Vec, bool],
    start: Vec,
    end: Vec,
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
                        step_into in walls,
                        weights.get(step_into),
                    )
                ):
                    continue

                weights[step_into] = step + 1
                queue.add(step_into)
        step += 1
    return weights[end]


def render_map(size: Vec, walls: dict[Vec, bool], path: set[Vec]):
    for y in range(size.y):
        vecs = (Vec(x, y) for x in range(size.x))
        print(
            "".join(
                "#" if vec in walls else "o" if vec in path else "." for vec in vecs
            )
        )


def part2():
    with open("input.txt") as f:
        bytes_ = f.readlines()
        bytes_ = list(map(str.strip, bytes_))

    low, high = 0, len(bytes_)
    while low < high:
        cursor = (low + high) // 2
        map_ = parse_map(bytes_, cursor)
        best_path = calculate_cheapest_path(Vec(70, 70), map_, Vec(0, 0), Vec(70, 70))
        print(bytes_[cursor], best_path)
        if best_path == 0:
            high = cursor - 1
        else:
            low = cursor + 1
    print(bytes_[cursor])


if __name__ == "__main__":
    part2()
    # with open("input.txt") as f:
    #     map_ = parse_map(map(str.strip, f), 1024)
    #     best_path = calculate_cheapest_path(Vec(70, 70), map_, Vec(0, 0), Vec(70, 70))
    #     print(best_path)
