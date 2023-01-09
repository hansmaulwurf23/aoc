import datetime
import re
from aopython import lcm

begin_time = datetime.datetime.now()
POSITIONS, INITIAL = range(2)

discs = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        discs.append(tuple(map(int, re.findall(r'\s\d+', line))))


def align(t, cycle, discno, discs):
    if discno > 0:
        cycle = lcm(cycle, discs[discno - 1][POSITIONS])
    while (t + 1 + discno + discs[discno][INITIAL]) % discs[discno][POSITIONS]:
        t += cycle

    if discno < len(discs) - 1:
        return align(t, cycle, discno + 1, discs)
    else:
        return t, cycle


t, cycle = align(0, 1, 0, discs)
print(f'part 1: {t}')
discs.append((11, 0))
t, cycle = align(t, cycle, len(discs)-1, discs)
print(f'part 2: {t}')
print(datetime.datetime.now() - begin_time)
