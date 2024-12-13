from typing import NamedTuple


class Machine(NamedTuple):
    a: tuple[int, int]
    b: tuple[int, int]
    prize: tuple[int, int]


def parse_machine(inp: tuple[str, str, str], p2: bool = False) -> Machine:
    btn_a = inp[0].split("+")
    btn_b = inp[1].split("+")
    prize = inp[2].split("=")

    if p2:
        extra_prize = 10000000000000
    else:
        extra_prize = 0

    return Machine(
        (int(btn_a[1].split(",")[0]), int(btn_a[2])),
        (int(btn_b[1].split(",")[0]), int(btn_b[2])),
        (int(prize[1].split(",")[0]) + extra_prize, int(prize[2]) + extra_prize),
    )


def solve_machine(machine: Machine):
    a1, a2 = machine.a
    b1, b2 = machine.b
    c1, c2 = machine.prize

    y = (c2 * a1 - c1 * a2) / (a1 * b2 - a2 * b1)
    x = (c1 - b1 * y) / a1
    return x, y


if __name__ == "__main__":
    with open("input.txt") as f:
        machines_str = f.read().split("\n\n")
        print(
            sum(
                map(
                    lambda a: a[0] * 3 + a[1],  # type: ignore
                    filter(
                        lambda a: (a[0] + a[1]) % 1 == 0,
                        map(
                            solve_machine,
                            map(
                                lambda m: parse_machine(tuple(m), True),  # type: ignore
                                map(lambda s: s.split("\n"), machines_str),
                            ),
                        ),
                    ),
                )
            )
        )
