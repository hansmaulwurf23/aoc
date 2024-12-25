import datetime
from collections import defaultdict
begin_time = datetime.datetime.now()

keys, locks = defaultdict(int), defaultdict(int)
with open('./input.txt') as f:
    blocks = f.read().split('\n\n')

    for block in blocks:
        store, k = (locks, '#') if all(c =='#' for c in block[0]) else (keys, '.')
        heights = [0] * 5
        for row in block.splitlines()[1:6]:
            for i, c in enumerate(row):
                heights[i] += 1 if c == k else 0
        store[tuple(heights)] += 1

p1 = 0
for l, c in locks.items():
    for kc in [keys[k] for k in keys if all(l <= k for l, k in zip(l, k))]:
        p1 += (c * kc)

print(p1)
print(datetime.datetime.now() - begin_time)
