import datetime
from collections import defaultdict
from aopython import min_max

begin_time = datetime.datetime.now()
crabs = defaultdict(int)
with open('./input.txt') as f:
    for v in map(int, f.readline().rstrip().split(',')):
        crabs[v] += 1

lo, hi = min_max(crabs.keys())
print(f'part 1: {min([sum(n * abs(pos - t) for pos, n in crabs.items()) for t in range(lo, hi + 1)])}')
print(f'part 2: {min([sum(n * abs(pos - t) * (abs(pos - t) + 1) // 2 for pos, n in crabs.items()) for t in range(lo, hi+1)])}')
print(datetime.datetime.now() - begin_time)
