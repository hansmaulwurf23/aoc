import datetime
import re
from collections import Counter

begin_time = datetime.datetime.now()
WEIGHT, HOLDS = range(2)
progs = dict()


def accu_weight(root):
    if progs[root][HOLDS]:
        sub_weights = dict()
        for h in progs[root][HOLDS]:
            sub_weights[h] = accu_weight(h)
        weight_counter = Counter(sub_weights.values())
        if len(weight_counter) > 1:
            wrong_weight = weight_counter.most_common(2)[1][0]
            print(f'wrongs {weight_counter} / {wrong_weight}')
            wrong_h = list([(n, w) for n, w in sub_weights.items() if w == wrong_weight])[0]
            diff = weight_counter.most_common(1)[0][0] - wrong_weight
            print(progs[wrong_h[0]][WEIGHT] + diff)
        return progs[root][WEIGHT] + (weight_counter.most_common(1)[0][0] * len(progs[root][HOLDS]))
    else:
        return progs[root][WEIGHT]


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        name, weight, holds = re.match(r'(\w+)+ \((\d+)\)( ->.*)?', line).groups()
        if holds:
            holds = set(holds.lstrip(' -> ').split(', '))
        progs[name] = (int(weight), holds)

holdings = set(filter(lambda x: progs[x][HOLDS], progs.keys()))
for h in holdings.copy():
    holdings -= progs[h][HOLDS]

root = holdings.pop()
accu_weight(root)
print(datetime.datetime.now() - begin_time)
