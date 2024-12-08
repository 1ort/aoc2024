from typing import Iterator, Iterable

def split_number_lists(in_: Iterable[str]) -> Iterable[Iterable[int]]:
    res = map(
            lambda tupl: tuple(map(int, tupl)),
            map(
                lambda x: x.split(" "),
                in_
            )
        )
    return map(tuple, res)

def is_safe(report: Iterable[int]) -> bool:
    print(report)
    report = iter(report)
    try:
        last_level = next(report)
        level = next(report)
        if not ( 1 <= abs(last_level - level) <= 3):
            print("not safe first two")
            return False
        last_sign = last_level > level
        last_level = level
    except StopIteration:
        print('safe StopIteration')
        return True
    for level in report:
        if not ((last_level > level) == last_sign and (1 <= abs(last_level - level) <= 3)):
            print('not safe')
            return False
        last_sign = last_level > level
        last_level = level
    print('safe')
    return True

def is_safe_tolerate(report: Iterable[int]) -> bool:
    print(report)
    report = iter(report)
    try:
        last_level = next(report)
    except StopIteration:
        return True # no values
    tolerated: bool = False
    last_sign = None

    for level in report:
        diff = last_level - level
        abs_diff = abs(diff)
        sign = diff > 0
        if last_level == level:
            if tolerated:
                print('unsafe same level', level, last_level, sign, last_sign)
                return False
            tolerated = True
            print('tolerated equal values')
        elif (last_sign is not None) and (last_level != level) and (last_sign != sign):
            if tolerated:
                print('unsafe wrong sign', level, last_level, sign, last_sign)
                return False
            tolerated = True
            print('tolerated wrong sign')
        elif not (1 <= abs_diff <= 3):
            if tolerated:
                print('unsafe abs diff', level, last_level, sign, last_sign)
                return False
            tolerated = True
            print('tolerated abs diff')
        if not tolerated:
            last_level = level
            last_sign = sign
    print('safe', tolerated)
    return True



def count_safe_reports(input: Iterable[str]) -> int:
    return sum(map(is_safe_tolerate, split_number_lists(input)))



if __name__ == "__main__":
    with open("input.txt", "r") as in_file:
        print(count_safe_reports(in_file))
