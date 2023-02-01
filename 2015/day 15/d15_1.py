import datetime
import re
from itertools import product

begin_time = datetime.datetime.now()

props = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        name = line.split(':')[0]
        cap, dur, fla, tex, cal = map(int, re.findall(r'-?\d+', line))
        props.append(tuple([cap, dur, fla, tex, cal]))

r = list(range(1, 101 - len(props)))
ingredient_count = len(props)
maxp = 0
max500 = 0
for seq in (seq for seq in product(r, repeat=ingredient_count) if sum(seq) == 100):
    prod = 1
    for p in range(4):
        s = max(0, sum([props[i][p] * amount for i, amount in enumerate(seq)]))
        if s == 0:
            prod = 0
            break
        prod *= s

    if maxp < prod:
        maxp = prod

    if max500 < prod and sum([props[i][-1] * amount for i, amount in enumerate(seq)]) == 500:
        max500 = prod


print(f'part 1: {maxp}')
print(f'part 2: {max500}')
print(datetime.datetime.now() - begin_time)
