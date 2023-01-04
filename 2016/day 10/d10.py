import datetime
import re
from collections import defaultdict
from functools import reduce

from aopython import dotdict

begin_time = datetime.datetime.now()
LOW, HIGH = range(2)
commands = []
bots = defaultdict(dotdict)
outputs = defaultdict(list)


def redistribute(b):
    q = [b]
    while q:
        idx = q.pop()
        fullbot = bots[idx]

        if 17 in fullbot.vals and 61 in fullbot.vals:
            print(f'17/61 {idx}')

        vals = [min(fullbot.vals), max(fullbot.vals)]
        for i, n in enumerate(fullbot.next):
            if n < 0:
                n = -(n + 1)
                outputs[n].append(vals[i])
            else:
                bots[n].vals.append(vals[i])
                if len(bots[n].vals) == 2:
                    q.append(n)


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        if line.startswith('bot'):
            b, lt, l, ht, h = re.match(r'bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)',
                                       line).groups()
            b, l, h = int(b), int(l), int(h)
            if lt == 'output': l = -1 - l
            if ht == 'output': h = -1 - h
            bots[b].next = (l, h)
            bots[b].vals = []

        elif line.startswith('value'):
            commands.append(tuple([int(x) for x in re.findall(r'\d+', line)]))

for v, b in commands:
    bots[b].vals.append(v)
    if len(bots[b].vals) == 2:
        redistribute(b)

print(reduce(lambda a, b: a * b, [outputs[o][0] for o in range(3)]))
print(datetime.datetime.now() - begin_time)
