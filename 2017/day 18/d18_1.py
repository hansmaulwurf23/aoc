import datetime
import re
from collections import defaultdict

begin_time = datetime.datetime.now()
regs = defaultdict(lambda: 0)

prog = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        prog.append(line.split(' '))

pc = 0
sound = None
recover = None
while 0 <= pc < len(prog):
    instr = prog[pc]
    op, x = instr[0], instr[1]
    if re.match(r'-?\d+', x):
        x = int(x)

    if len(instr) == 3:
        y = int(instr[2]) if re.match(r'-?\d+', instr[2]) else regs[instr[2]]

    if op == 'snd':
        sound = regs[x]
        pc += 1
    elif op == 'set':
        regs[x] = y
        pc += 1
    elif op == 'add':
        regs[x] += y
        pc += 1
    elif op == 'mul':
        regs[x] *= y
        pc += 1
    elif op == 'mod':
        regs[x] %= y
        pc += 1
    elif op == 'rcv':
        if regs[x] > 0:
            recover = sound
            print(recover)
            break
        pc += 1
    elif op == 'jgz':
        if (type(x) == int and x > 0) or regs[x] > 0:
            pc += y
        else:
            pc += 1


print(datetime.datetime.now() - begin_time)
