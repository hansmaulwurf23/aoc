import datetime
from collections import Counter, defaultdict
from functools import cache
from itertools import pairwise

from aopython import mapSum

begin_time = datetime.datetime.now()

rules = {}
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        poly = list(line)

    while line := f.readline().rstrip():
        ma, ins = line.split(' -> ')
        rules[ma] = ins


@cache
def grow(m, n, restSteps):
    if restSteps <= 0:
        return
    else:
        new = rules[m+n]
        creations = defaultdict(int)
        creations[new] += 1

        mapSum(creations, grow(m, new, restSteps - 1))
        mapSum(creations, grow(new, n, restSteps - 1))

        return creations


countings = mapSum(defaultdict(int), Counter(poly))
for m, n in pairwise(poly):
    mapSum(countings, grow(m, n, 40))

c = Counter(countings)
print(f'part 2: {c.most_common(1)[0][1] - c.most_common()[-1][1]}')
print(datetime.datetime.now() - begin_time)
