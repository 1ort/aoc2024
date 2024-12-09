def process(inp: str) -> int:
    disk = list(map(int, inp.strip()))

    empty_sector_cursor = 1
    last_file_cursor = len(disk) - 1

    result_cursor = disk[0]
    checksum = 0

    while empty_sector_cursor < last_file_cursor:
        empty_sector_size = disk[empty_sector_cursor]
        last_file_size = disk[last_file_cursor]
        last_file_id = (last_file_cursor) // 2

        if empty_sector_size <= last_file_size:
            checksum += sum(
                [
                    pos * last_file_id
                    for pos in range(result_cursor, result_cursor + empty_sector_size)
                ]
            )
            result_cursor += empty_sector_size

            next_file_cursor = empty_sector_cursor + 1
            next_file_id = next_file_cursor // 2
            next_file_size = disk[next_file_cursor]
            checksum += sum(
                [
                    pos * next_file_id
                    for pos in range(result_cursor, result_cursor + next_file_size)
                ]
            )
            result_cursor += next_file_size

            disk[last_file_cursor] -= empty_sector_size
            if empty_sector_size == last_file_size:
                last_file_cursor -= 2
            empty_sector_cursor += 2

        elif empty_sector_size > last_file_size:
            disk[empty_sector_cursor] -= last_file_size
            checksum += sum(
                [
                    pos * last_file_id
                    for pos in range(result_cursor, result_cursor + last_file_size)
                ]
            )
            result_cursor += last_file_size
            last_file_cursor -= 2
    return checksum


if __name__ == "__main__":
    with open("input.txt") as f:
        print(process(f.read()))
