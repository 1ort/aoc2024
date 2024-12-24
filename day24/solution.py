from collections import deque
from typing import Iterable, NamedTuple
from itertools import chain, takewhile


class Instruction(NamedTuple):
    name: str
    value: bool | tuple[str, str, str]


def process_instructions(ins: Iterable[Instruction]) -> dict[str, bool]:
    mem: dict[str, bool] = {}
    queue = deque(ins)
    while queue:
        instruction = queue.popleft()
        match instruction:
            case Instruction(name, bool(literal_value)):
                mem[name] = literal_value
            case Instruction(name, (a, 'AND', b)):
                if a not in mem or b not in mem:
                    queue.append(instruction)
                    continue
                mem[name] = mem[a] and mem[b]
            case Instruction(name, (a, 'OR', b)):
                if a not in mem or b not in mem:
                    queue.append(instruction)
                    continue
                mem[name] = mem[a] or mem[b]
            case Instruction(name, (a, 'XOR', b)):
                if a not in mem or b not in mem:
                    queue.append(instruction)
                    continue
                mem[name] = mem[a] ^ mem[b]
    return mem


def parse_input(inp: Iterable[str]) -> Iterable[Instruction]:
    inp = map(str.strip, inp)

    inp = iter(inp)

    def parse_literal(line: str):
        name, val = line.split(': ')
        return Instruction(
            name,
            bool(int(val)),
        )

    literals = takewhile(bool, inp)
    literals = (parse_literal(line) for line in literals)

    def parse_instruction(line: str):
        rest, name = line.split(' -> ')
        a, op, b = rest.split()
        return Instruction(
            name,
            (a, op, b),
        )

    instructions = (parse_instruction(line) for line in inp)
    return chain(literals, instructions)


if __name__ == '__main__':
    with open('input.txt') as f:
        ins = parse_input(f)
        mem = process_instructions(ins)

        binary = ''.join(
            str(int(mem[k])) for k in sorted(item for item in mem if item.startswith('z'))
        )[::-1]
        print(int(binary, 2))
