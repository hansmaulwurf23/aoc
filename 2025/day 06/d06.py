import datetime
from functools import reduce

begin_time = datetime.datetime.now()

OPS = {
    '+': lambda a, b: a + b,
    '*': lambda a, b: a * b,
}


def part1(lines):
    operands, gts = [], 0
    for line in [l[:-1] for l in lines[:-1]]:
        operands.append(list(map(int, line.split())))
    operators = lines[-1].split()

    for op, *ops in zip(operators, *operands):
        gts += reduce(OPS[op], ops)

    assert gts in (6209956042374, 4277556)
    return gts


def part2(lines):
    operands, gts = [], 0
    operators = lines[-1].split()

    ops, eqidx = [], 0
    for line in [''.join(l).strip() for l in zip(*lines[:-1])]:
        if line:
            ops.append(int(line))
        else:
            gts += reduce(OPS[operators[eqidx]], ops)
            eqidx += 1
            ops = []

    assert gts in (12608160008022, 3263827)
    return gts


with open('./input.txt') as f:
    lines = f.readlines()

print(f'Part 1: {part1(lines)}')
print(f'Part 2: {part2(lines)}')
print(datetime.datetime.now() - begin_time)
