def count_xmas2(inp: str) -> int:
    xmas = "XMAS"
    xmas_count = 0
    row_len = len(inp.split('\n', maxsplit=1)[0])
    xmas_len = len(xmas)
    joined = "".join(inp.split("\n"))

    for i, char in enumerate(joined):
        current_pos_in_row = i % row_len
        if char == xmas[0]:
            if current_pos_in_row <= (row_len - xmas_len):
                # check inside row
                possible_xmas = joined[i:i+xmas_len]
                if possible_xmas == xmas:
                    xmas_count += 1
                # check left to right diagonals
                possible_diagonal_xmas = joined[i:i+(row_len+1)*(xmas_len-1)+1:row_len+1]
                if possible_diagonal_xmas == xmas:
                    xmas_count += 1

            if current_pos_in_row >= xmas_len - 1:
                # check right to left down diagonals
                possible_diagonal_xmas = joined[i:i+(row_len-1)*(xmas_len-1)+1:row_len-1]
                if possible_diagonal_xmas == xmas:
                    xmas_count += 1
            # check column
            possible_vertical_xmas = joined[i:i+(row_len)*(xmas_len-1)+1:row_len]
            if possible_vertical_xmas == xmas:
                    xmas_count += 1
    return xmas_count

def count_x_mas(inp: str) -> int:
    mas = "MAS"
    x_mas_count = 0
    row_len = len(inp.split('\n', maxsplit=1)[0])
    mas_len = len(mas)
    joined = "".join(inp.split("\n"))

    for i, char in enumerate(joined):
        current_pos_in_row = i % row_len
        if 0 < current_pos_in_row < (row_len - 1):
            if char == mas[1]:
                possible_mas_start = i - (row_len + 1)
                possible_mas_end = i + (row_len + 1)
                possible_right_diagonal = joined[possible_mas_start:possible_mas_end+1:row_len+1]

                possible_mas_start = i - (row_len - 1)
                possible_mas_end = i + (row_len - 1)
                possible_left_diagonal = joined[possible_mas_start:possible_mas_end+1:row_len-1]

                if possible_right_diagonal in {mas, mas[::-1]} and possible_left_diagonal in {mas, mas[::-1]}:
                    x_mas_count += 1
    return x_mas_count


if __name__ == "__main__":
    with open("input.txt") as f:
        inp = f.read().strip()
        res_direct = count_xmas2(inp)
        res_reversed = count_xmas2(inp[::-1])
        print(f"{res_direct} + {res_reversed} = {res_direct + res_reversed}")

    with open("input.txt") as f:
        inp = f.read().strip()
        print('x_max:', count_x_mas(inp))
