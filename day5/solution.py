from functools import cmp_to_key
from typing import Iterable
from itertools import takewhile

def process_lines(lines: Iterable[str]):
    result = 0
    lines = iter(lines)
    rules = takewhile(bool, lines)
    lines = takewhile(bool, lines)
    
    constraints : list[tuple[int, int]] = []
    for rule in rules:
        print(repr(rule))
        constraints.append(tuple(map(int, rule.split("|")))) # type: ignore[reportArgumentType]

    for line in lines:
        print(repr(line))
        nums = list(map(int, line.split(",")))
        pos = {}
        for i, num in enumerate(nums):
            pos[num] = i

        for first, second in constraints:
            if first in pos and second in pos:
                if pos[first] >= pos[second]:
                    break
        else:
            # all numbers in correct order
            print(nums)
            middle_num = nums[len(nums)//2]
            print(middle_num)
            result += middle_num
    return result

def process_with_correction(lines: Iterable[str]):
    result = 0
    lines = iter(lines)
    rules = takewhile(bool, lines)
    lines = takewhile(bool, lines)

    constraints : list[tuple[int, int]] = []

    def constraints_sort_key(a: int, b: int) -> int:
        for (first, second) in constraints:
            if a == first and b == second:
                return -1
            if a == second and b == first:
                return 1
        return 0


    for rule in rules:
        print(repr(rule))
        constraints.append(tuple(map(int, rule.split("|")))) # type: ignore[reportArgumentType]
    for line in lines:
        print(repr(line))
        nums = list(map(int, line.split(",")))
        pos = {}
        for i, num in enumerate(nums):
            pos[num] = i

        for first, second in constraints:
            if first in pos and second in pos:
                if pos[first] >= pos[second]:
                    nums.sort(key=cmp_to_key(constraints_sort_key))
                    break
        else:
            continue
         # all numbers in correct order
        print(nums)
        middle_num = nums[len(nums)//2]
        print(middle_num)
        result += middle_num
    return result


if __name__ == "__main__":
    with open('input.txt') as f:
        print(process_with_correction(f.read().split("\n")))

