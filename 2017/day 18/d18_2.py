import datetime
import re
from collections import defaultdict, deque

begin_time = datetime.datetime.now()
reg_banks = [defaultdict(lambda: 0), defaultdict(lambda: 0)]

prog = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        prog.append(line.split(' '))

pcs = [0, 0]
msg_qs = [deque(), deque()]
prog_id = 0
reg_banks[1]['p'] = 1
pc = pcs[prog_id]
regs = reg_banks[prog_id]
send_count = 0

while 0 <= pc < len(prog):
    instr = prog[pc]
    op, x = instr[0], instr[1]
    if re.match(r'-?\d+', x):
        x = int(x)

    if len(instr) == 3:
        y = int(instr[2]) if re.match(r'-?\d+', instr[2]) else regs[instr[2]]

    if op == 'snd':
        msg_qs[(prog_id + 1) % 2].append(regs[x])
        if prog_id == 1:
            send_count += 1
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
        if len(msg_qs[prog_id]):
            regs[x] = msg_qs[prog_id].popleft()
            pc += 1
        else:
            pcs[prog_id] = pc
            prog_id = (prog_id + 1) % 2
            regs = reg_banks[prog_id]
            pc = pcs[prog_id]
            print(f'switched context to {prog_id} msg_qs: {len(msg_qs[0])} / {len(msg_qs[1])}')

            if prog[pc][0] == 'rcv' and len(msg_qs[prog_id]) == 0:
                break
    elif op == 'jgz':
        if regs[x] > 0:
            pc += y
        else:
            pc += 1

print(send_count)
print(datetime.datetime.now() - begin_time)
