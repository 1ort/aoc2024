def evolve_secret_number(num: int) -> int:
    num = prune(mix(num, num * 64))
    num = prune(mix(num, num // 32))
    num = prune(mix(num, num * 2048))

    return num


def mix(num: int, a: int) -> int:
    return num ^ a


def prune(num: int) -> int:
    return num % 16777216


if __name__ == "__main__":
    with open("input.txt") as f:
        f = map(int, map(str.strip, f.readlines()))
    result = 0
    for num in f:
        for _ in range(2000):
            num = evolve_secret_number(num)
        print(num)
        result += num
    print(result)
