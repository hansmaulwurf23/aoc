import datetime
import re
from collections import defaultdict

begin_time = datetime.datetime.now()
regs = defaultdict(lambda: 0)
regs['a'] = 1

prog = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        prog.append(line.split(' '))


def run_raw():
    pc = 0
    while 0 <= pc < len(prog):
        instr = prog[pc]
        op, x = instr[0], instr[1]
        if re.match(r'-?\d+', x):
            x = int(x)

        if len(instr) == 3:
            y = int(instr[2]) if re.match(r'-?\d+', instr[2]) else regs[instr[2]]

        if op == 'set':
            regs[x] = y
            pc += 1
        elif op == 'sub':
            regs[x] -= y
            pc += 1
        elif op == 'mul':
            regs[x] *= y
            pc += 1
        elif op == 'jnz':
            if (type(x) == int and x != 0) or regs[x] != 0:
                pc += y
            else:
                pc += 1
        else:
            print(f'unknown op {op} / {x} / {y}')
    return regs['h']

def run_smart():
    h = 0
    b = 105700
    c = b + 17000

    for n in range(b, c + 1, 17):
        fac = 2
        while fac * fac <= n:
            if n % fac == 0:
                break
            fac += 1
        if n % fac == 0:
            h += 1

    return h


def run():
    h = 0
    b, c = 57, 57
    b = b * 100 + 100000
    c = b + 17000
    while True:
        f, d = 1, 2
        while True:
            e = 2
            while True:
                g = d * e - b
                # g == 0 if d * e == b -> b must be divisible since d, e start with 2
                # and are incremented by one and the two loops stop when d, e == b
                if g == 0:
                    f = 0
                e += 1
                g = e - b
                if g == 0:
                    break
            d += 1
            g = d - b
            if g == 0:
                break

        # f is only set to zero in the innermost loop, and only if b = d * e, which means b
        # is not a prime -> run_smart() is the faster implementation
        if f == 0:
            h += 1
        g = b - c
        print(g)
        if g == 0:
            return h
        # [A] c is never updated -> initially c - b = 17000 -> loop has to run 1000 times until b = c
        b += 17


print(run_smart())
print(datetime.datetime.now() - begin_time)
