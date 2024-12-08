import re

mul_re = re.compile(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)")

switched_re = re.compile(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)|do\(\)|don't\(\)")


def mul(a, b):
    return a * b

def eval_instructions(inp: str) -> int:
    res = 0
    for match in  mul_re.finditer(inp):
        res += mul(*map(int, match.groups()))
    return res
    
def eval_switchable_instructions(inp: str) -> int:
    res = 0
    enabled = True

    for match in switched_re.finditer(inp):
        if match.group(0) == r"do()":
            enabled = True
        elif match.group(0) == r"don't()":
            enabled = False
        else:
            if enabled:
                res += mul(*map(int, match.groups()))
    return res



if __name__ == "__main__":
    with open("input.txt") as f:
        print(eval_switchable_instructions(f.read()))
