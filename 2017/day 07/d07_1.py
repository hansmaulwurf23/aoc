import datetime
import re

begin_time = datetime.datetime.now()
WEIGHT, HOLDS = range(2)

progs = dict()
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        name, weight, holds = re.match(r'(\w+)+ \((\d+)\)( ->.*)?', line).groups()
        if holds:
            holds = set(holds.lstrip(' -> ').split(', '))
        progs[name] = (int(weight), holds)

holdings = set(filter(lambda x: progs[x][HOLDS], progs.keys()))
for h in holdings.copy():
    holdings -= progs[h][HOLDS]

print(holdings.pop())
print(datetime.datetime.now() - begin_time)
