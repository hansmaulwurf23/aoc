import datetime
import math
import re

begin_time = datetime.datetime.now()

ADDR, ADDI, MULR, MULI, BANR, BANI, BORR, BORI, SETR, SETI, GTIR, GTRI, GTRR, EQIR, EQRI, EQRR = range(16)
op_codes = {'addr': 0, 'addi': 1, 'mulr': 2, 'muli': 3, 'banr': 4, 'bani': 5, 'borr': 6, 'bori': 7, 'setr': 8,
            'seti': 9, 'gtir': 10, 'gtri': 11, 'gtrr': 12, 'eqir': 13, 'eqri': 14, 'eqrr': 15}
op_names = {v:k for k, v in op_codes.items()}


def read_program(lines):
    instr = []
    for l in lines:
        op, args = l.split(' ', maxsplit=1)
        instr.append(tuple([op_codes[op]] + list(map(int, re.findall(r'\d+', l)))))

    return instr


def run_program(program, ip_reg):
    regs = [1, 0, 0, 0, 0, 0]
    pc = 0

    while pc < len(program):
        regs[ip_reg] = pc
        op, a, b, c = program[pc]

        if op == ADDR:
            regs[c] = regs[a] + regs[b]
        elif op == ADDI:
            regs[c] = regs[a] + b
        elif op == MULR:
            regs[c] = regs[a] * regs[b]
        elif op == MULI:
            regs[c] = regs[a] * b
        elif op == BANR:
            regs[c] = regs[a] & regs[b]
        elif op == BANI:
            regs[c] = regs[a] & b
        elif op == BORR:
            regs[c] = regs[a] | regs[b]
        elif op == BORI:
            regs[c] = regs[a] | b
        elif op == SETR:
            regs[c] = regs[a]
        elif op == SETI:
            regs[c] = a
        elif op == GTIR:
            regs[c] = (1 if a > regs[b] else 0)
        elif op == GTRI:
            regs[c] = (1 if regs[a] > b else 0)
        elif op == GTRR:
            regs[c] = (1 if regs[a] > regs[b] else 0)
        elif op == EQIR:
            regs[c] = (1 if a == regs[b] else 0)
        elif op == EQRI:
            regs[c] = (1 if regs[a] == b else 0)
        elif op == EQRR:
            regs[c] = (1 if regs[a] == regs[b] else 0)

        pc = regs[ip_reg]
        pc += 1

    return regs[0]


with open('./input.txt') as f:
    lines = f.readlines()

ip_reg = int(re.findall(r'\d+', lines[0])[0])
script = read_program(lines[1:])
# print(run_program(script, ip_reg))

# v = 10551367
#    lines 17 to 20  and 21 to 24
v = (2 * 2 * 19 * 11) + (5 * 22 + 21)
# line33 + lines 28 to 32
v = v + (27 * 28 + 29) * 30 * 14 * 32
# v= 967
result = 1 + v
f = 2
while f * f <= v:
    if v % f:
        f += 1
    else:
        v //= f
        result += f
if v > 1:
    result += v

print(result)
print(datetime.datetime.now() - begin_time)
