from dataclasses import dataclass
from typing import Iterable, assert_never


@dataclass
class Computer:
    a: int
    b: int
    c: int

    write_buff: list[int]

    mem: list[int]
    pointer: int = 0

    def run(self):
        self.pointer = 0
        self.write_buff = []
        while True:
            if self.pointer > len(self.mem) - 2:
                break
            op, operand = self.mem[self.pointer : self.pointer + 2]

            operator = {
                0: self.adv,
                1: self.bxl,
                2: self.bst,
                3: self.jnz,
                4: self.bxc,
                5: self.out,
                6: self.bdv,
                7: self.cdv,
            }[op]

            jump_to = operator(operand)
            if jump_to is not None:
                self.pointer = jump_to
            else:
                self.pointer += 2

        return self.write_buff

    def adv(self, operand):
        numerator = self.a
        denomenator = 2 ** self.get_combo_operand(operand)
        self.a = int(numerator // denomenator)

    def bxl(self, operand):
        self.b = self.b ^ operand

    def bst(self, operand):
        self.b = self.get_combo_operand(operand) % 8

    def jnz(self, operand):
        if self.a == 0:
            return
        return operand

    def bxc(self, operand):
        self.b = self.b ^ self.c

    def out(self, operand):
        self.write_buff.append(self.get_combo_operand(operand) % 8)

    def bdv(self, operand):
        numerator = self.a
        denomenator = 2 ** self.get_combo_operand(operand)
        self.b = int(numerator // denomenator)

    def cdv(self, operand):
        numerator = self.a
        denomenator = 2 ** self.get_combo_operand(operand)
        self.c = int(numerator // denomenator)

    def get_combo_operand(self, operand: int) -> int:
        if operand == 7:
            raise RuntimeError(
                "Combo operand 7 is reserved and must not appear in valid programs"
            )
        return {4: self.a, 5: self.b, 6: self.c}.get(operand, operand)


def parse_cpu(f: Iterable[str]) -> Computer:
    f = map(str.strip, f)
    register_a = next(f).rsplit(" ", maxsplit=1)[-1]
    register_b = next(f).rsplit(" ", maxsplit=1)[-1]
    register_c = next(f).rsplit(" ", maxsplit=1)[-1]

    assert next(f) == ""

    memory = next(f).rsplit(" ", maxsplit=1)[-1].split(",")
    memory = list(map(int, memory))

    return Computer(
        a=int(register_a),
        b=int(register_b),
        c=int(register_c),
        mem=memory,
        write_buff=[],
        pointer=0,
    )


def find_register_value(comp: Computer):
    b, c = comp.b, comp.c
    for i in range(0, 64):
        comp.a = i
        comp.b = b
        comp.c = c

        res = comp.run()
        print(i, res)
        if res == comp.mem:
            break


if __name__ == "__main__":
    with open("input.txt") as f:
        cpu = parse_cpu(f)
        print(find_register_value(cpu))
