import datetime
import re
from collections import defaultdict

begin_time = datetime.datetime.now()
regs = defaultdict(lambda: 0)

prog = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        prog.append(line.split(' '))


def run_raw():
    pc = 0
    muls = 0
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
            muls += 1
            regs[x] *= y
            pc += 1
        elif op == 'jnz':
            if (type(x) == int and x != 0) or regs[x] != 0:
                pc += y
            else:
                pc += 1
        else:
            print(f'unknown op {op} / {x} / {y}')
    return muls


def run():
    muls = 0
    h = 0
    b, c = 57, 57
    while True:
        f, d = 1, 2
        while True:
            e = 2
            while True:
                muls += 1
                g = d * e - b
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
        if f == 0:
            h += 1
        g = b - c
        if g == 0:
            return muls
        b += 17


print(run())
print(datetime.datetime.now() - begin_time)
