from functools import cache
from itertools import permutations

numeric_coords = {
    "0": (1, 3),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "A": (2, 3),
    "None": (0, 3),
}

directional_coords = {
    "^": (1, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
    "A": (2, 0),
    "None": (0, 0),
}

moves_to_keys = {
    (0, 1): "v",
    (0, -1): "^",
    (1, 0): ">",
    (-1, 0): "<",
}


# This function did'nt work for me :(
def build_sequense(cords: dict, code: str, position) -> str:
    result_sequense = []

    for key in code:
        key_position = cords[key]
        delta = (key_position[0] - position[0], key_position[1] - position[1])
        if (key_position[0], position[1]) == cords["None"]:
            result_sequense.extend(["v" if delta[1] > 0 else "^"] * abs(delta[1]))
            result_sequense.extend([">" if delta[0] > 0 else "<"] * abs(delta[0]))
        else:
            result_sequense.extend([">" if delta[0] > 0 else "<"] * abs(delta[0]))
            result_sequense.extend(["v" if delta[1] > 0 else "^"] * abs(delta[1]))
        result_sequense.append("A")
        position = key_position

    return "".join(result_sequense)


def summarize_moves(start, moves: list[tuple[int, int]]):
    return (
        start[0] + sum(move[0] for move in moves),
        start[1] + sum(move[1] for move in moves),
    )


def all_movesets(from_, to_, cords):
    delta = (to_[0] - from_[0], to_[1] - from_[1])
    result_sequense = []
    result_sequense.extend([(0, 1) if delta[1] > 0 else (0, -1)] * abs(delta[1]))
    result_sequense.extend([(1, 0) if delta[0] > 0 else (-1, 0)] * abs(delta[0]))

    sets = [
        "".join([moves_to_keys[key] for key in moveset]) + "A"
        for moveset in set(permutations(result_sequense))
        if not any(
            summarize_moves(from_, moveset[:i]) == cords["None"]
            for i in range(len(moveset))
        )
    ]
    return sets or ["A"]


@cache
def minimal_len(code: str, max_depth=25, depth=0):
    cords = directional_coords if depth > 0 else numeric_coords
    length = 0
    position = cords["A"]

    for key in code:
        key_position = cords[key]

        movesets = all_movesets(position, key_position, cords)
        if depth == max_depth:
            length += len(movesets[0])
        else:
            length += min(
                minimal_len(moveset, max_depth, depth + 1) for moveset in movesets
            )
        position = key_position

    return length


def calculate_complexity(num_code: str) -> int:
    code_len = minimal_len(num_code)

    print(num_code[:-1], code_len)
    return int(num_code[:-1]) * code_len


if __name__ == "__main__":
    with open("input.txt") as f:
        f = list(map(str.strip, f))

    result = 0
    for code in f:
        print(code)
        res = calculate_complexity(code)
        result += res
    print(result)
