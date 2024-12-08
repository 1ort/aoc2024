from collections import Counter
from typing import Iterable, Iterator
from  itertools import tee

def split_number_lists(in_: Iterable[str]) -> tuple[Iterator[int], ...]:
    res = map(
            lambda tupl: tuple(map(int, tupl)),
            map(
                lambda x: x.split("   "),
                in_
            )
        )
    return tuple(zip(*res))
 
def calculate_distance(in_: Iterable[str]) -> int:
    num_lists = split_number_lists(in_)
    return sum(
        map(
            lambda tupl: abs(tupl[0] - tupl[1]),
            zip(
                *map(
                    sorted,
                    num_lists
                )
            )
        )
    )

def calculate_similarity_score(in_: Iterable[str]) -> int:
    num_lists = split_number_lists(in_) 
    counter = Counter(num_lists[1])
    return sum(
        counter[x] * x for x in num_lists[0]
    )

if __name__ == "__main__":
    with open("input.txt", "r") as in_file:
        print(calculate_similarity_score(in_file))
