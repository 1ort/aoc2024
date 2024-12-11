from collections import Counter, defaultdict


# part 1 naive attempt
def evolve_stones(stones: list[str]):
    for pos in range(len(stones) - 1, -1, -1):
        stone_num = stones[pos]
        if stone_num == "0":
            stones[pos] = "1"
            continue

        digits = len(stone_num)
        if len(stone_num) % 2 == 0:
            stones[pos : pos + 1] = list(
                map(
                    lambda x: x.lstrip("0") or "0",
                    [stone_num[: digits // 2], stone_num[digits // 2 :]],
                )
            )
        else:
            stones[pos] = str(int(stone_num) * 2024)


# part 2
def simulate_evolve_stones(stones: dict[int, int]) -> dict[int, int]:
    result = defaultdict(int)

    for stone in stones:
        if stone == 0:
            result[1] += stones[stone]
        elif len(str(stone)) % 2 == 0:
            str_ = str(stone)
            digits = len(str_)

            result[int(str_[: digits // 2])] += stones[stone]
            result[int(str_[digits // 2 :])] += stones[stone]
        else:
            result[stone * 2024] += stones[stone]

    return result


if __name__ == "__main__":
    with open("input.txt") as f:
        stones = map(int, list(f.read().strip().split()))
        stones = Counter(stones)
        print(stones)
        for i in range(75):
            stones = simulate_evolve_stones(stones)
            print(i, stones, sum(stones.values()))
