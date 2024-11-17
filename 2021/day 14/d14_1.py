import datetime
from collections import Counter
from itertools import pairwise

begin_time = datetime.datetime.now()

rules = {}
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        poly = list(line)

    while line := f.readline().rstrip():
        ma, ins = line.split(' -> ')
        rules[ma] = ins

for s in range(10):
    res = []
    for x in pairwise(poly):
        res.extend([x[0], rules[x[0] + x[1]]])
    res.append(poly[-1])
    poly = res

c = Counter(poly)
print(f'part 1: {c.most_common(1)[0][1] - c.most_common()[-1][1]}')
print(datetime.datetime.now() - begin_time)
