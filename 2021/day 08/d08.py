import datetime
from collections import defaultdict
from functools import reduce

begin_time = datetime.datetime.now()

lengths = defaultdict(int)
entries = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        patterns, outputs = map(lambda x: x.split(), line.split(' | '))
        for output in outputs:
            lengths[len(output)] += 1
        entries.append((map(frozenset, patterns), map(frozenset, outputs)))

print(f'part 1: {lengths[2] + lengths[4] + lengths[3] + lengths[7]}')

result = 0
for patterns, outputs in entries:
    digits = dict()
    lens = defaultdict(lambda: frozenset('abcdefg'))

    for o in patterns:
        lens[len(o)] &= o

    a = lens[3] - lens[2]
    bd = lens[4] - lens[2]
    eg = lens[7] - lens[4] - a
    dg = lens[5] - a
    g = eg & dg
    d = dg - g
    abfg = lens[6]
    bf = abfg - a - g

    digits[lens[7] - d] = 0
    digits[lens[2]] = 1
    digits[lens[7] - bf] = 2
    digits[lens[3] | dg] = 3
    digits[lens[4]] = 4
    digits[abfg | d] = 5
    digits[abfg | d | eg] = 6
    digits[lens[3]] = 7
    digits[lens[7]] = 8
    digits[lens[4] | a | g] = 9

    val = 0
    for o in outputs:
        val = (val * 10) + digits[o]
    result += val

print(f'part 2: {result}')
print(datetime.datetime.now() - begin_time)
