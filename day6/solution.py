from collections import defaultdict
from typing import Any, Iterable
from itertools import repeat

def parse_map(rows: Iterable[str]) -> tuple[set[tuple[int, int]], tuple[int, int]]:
    guard_pos = (-1, -1)
    obstacles = set[tuple[int, int]]()

    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char == "^":
                guard_pos = (x, y)
            if char == "#":
                obstacles.add((x, y))
    return obstacles, guard_pos


def calculate_movement(obstacles: set[tuple[int, int]], current_position: tuple[int, int], direction: int = 1) -> int:
    visited = {current_position}

    # 1 - up
    # 2 - right
    # 3 - down
    # 4 - left
    next_direction = {
        1: 2,
        2: 3,
        3: 4,
        4: 1,
    }

    visited_obstacles_by_directions: dict[int, set[tuple[int, int]]] = defaultdict(set)

    max_x = max(obstacles, key=lambda pos: pos[0])[0]
    max_y = max(obstacles, key=lambda pos: pos[1])[1]
    while True:
        current_x = current_position[0]
        current_y = current_position[1]

        direction_loop = {
            1: zip(repeat(current_x), range(current_y-1, -1, -1)),
            2: zip(range(current_x+1, max_x+1, 1), repeat(current_y)),
            3: zip(repeat(current_x), range(current_y+1, max_y+1, 1)),
            4: zip(range(current_x-1, -1, -1), repeat(current_y)),
        }[direction]
        for x, y in direction_loop:
            if (x, y) in obstacles:
                if (x, y) in visited_obstacles_by_directions[direction]:
                    raise RuntimeError('has loop')
                visited_obstacles_by_directions[direction].add((x, y))
                direction = next_direction[direction]
                break
            else:
                visited.add((x, y))
                current_position = (x, y)
        else:
            break   # exited map
    return len(visited)

def count_obstructions(obstacles: set[tuple[int, int]], current_position: tuple[int, int], direction: int = 1) -> int:
    visited = {current_position}
    # 1 - up
    # 2 - right
    # 3 - down
    # 4 - left
    next_direction = {
        1: 2,
        2: 3,
        3: 4,
        4: 1,
    }

    possible_obstruictions = set()

    visited_obstacles_by_directions: dict[int, set[tuple[int, int]]] = defaultdict(set)

    max_x = max(obstacles, key=lambda pos: pos[0])[0]
    max_y = max(obstacles, key=lambda pos: pos[1])[1]
    while True:
        current_x = current_position[0]
        current_y = current_position[1]

        direction_loop = {
            1: zip(repeat(current_x), range(current_y-1, -1, -1)),
            2: zip(range(current_x+1, max_x+1, 1), repeat(current_y)),
            3: zip(repeat(current_x), range(current_y+1, max_y+1, 1)),
            4: zip(range(current_x-1, -1, -1), repeat(current_y)),
        }[direction]
        for x, y in direction_loop:
            if (x, y) in obstacles:
                visited_obstacles_by_directions[direction].add((x, y))
                direction = next_direction[direction]
                break
            else:
                last_position = current_position
                current_position = (x, y)
                if current_position not in visited:
                    visited.add(current_position)
                    try:
                        calculate_movement(
                           obstacles | {current_position},
                            last_position,
                            next_direction[direction],
                        )
                    except RuntimeError:
                        possible_obstruictions.add((x, y))

        else:
            break   # exited map
    return len(possible_obstruictions)



# Для части 2 нужно менять текущее положение гварда как обычно и на каждый шаг ставить блок перед собой и смотреть,
# вызывает ли он цикл
# Проверку цикла нужно добавить в функцию, записывая, с какой стороны в какое препятствие мы уже врезались

if __name__ == "__main__":
    with open("input.txt") as f:
        obstacles, current_position = parse_map(map(str.strip, f.readlines()))
        print(count_obstructions(obstacles, current_position))
