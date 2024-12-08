from typing import Iterable

def is_solvable(result, nums: list[int]) -> bool:
    if len(nums) == 1:
        return result == nums[0]

    if len(nums) == 2:
        return result == sum(nums) or result == nums[0] * nums[1] or result == int(f"{nums[0]}{nums[1]}")

    return (
        is_solvable(
            result,
            [nums[0] + nums[1]] + nums[2:]
        )
        or
        is_solvable(
            result,
            [nums[0] * nums[1]] + nums[2:]
        )
        or
        is_solvable(
            result,
            [int(f"{nums[0]}{nums[1]}")] + nums[2:]
        )
    )


def parse_line(raw_line: str) -> tuple[int, list[int]]:
    line = raw_line.strip().split(':', maxsplit=1)

    result = int(line[0])
    nums = map(
        int,
        line[1].split()
    )
    return (result, list(nums))


def process_lines(lines: Iterable[str]) -> int:
    return sum(
        map(
            lambda tupl: tupl[0] if is_solvable(*tupl) else 0,
            map(parse_line, lines)
        )
    )


if __name__ == "__main__":
    with open("input_example.txt") as f:
        print(process_lines(f)) 
