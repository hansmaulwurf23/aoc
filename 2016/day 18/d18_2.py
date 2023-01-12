import datetime
from collections import Counter
from itertools import product

begin_time = datetime.datetime.now()
MAP_WIDTH = None
PATTERN_SIZE = 10  # must be such that MAP_WIDTH % PATTERN_SIZE == 0!
CACHE = None


def add_row(last_row):
    last = list(last_row)
    last.insert(0, '.')
    last.append('.')
    new_row = []
    for i in range(MAP_WIDTH // PATTERN_SIZE):
        new_row.extend(CACHE[tuple(last[i * PATTERN_SIZE:(i + 1) * PATTERN_SIZE + 2])])
    return new_row


def prepare_cache():
    psize = PATTERN_SIZE + 2
    cache = dict()
    for t in product(['.', '^'], repeat=psize):
        result = []
        for i in range(1, psize - 1):
            a = t[i - 1]
            c = t[i + 1]
            if (a == '^' and c == '.') or (c == '^' and a == '.'):
                result.append('^')
            else:
                result.append('.')
        cache[tuple(t)] = result
    return cache


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        last_row = tuple(line)
        MAP_WIDTH = len(last_row)

CACHE = prepare_cache()
s = 0
for i in range(400000):
    s += Counter(last_row)['.']
    last_row = add_row(last_row)

print(s)
print(datetime.datetime.now() - begin_time)
