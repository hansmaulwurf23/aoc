import datetime
from collections import defaultdict, deque

begin_time = datetime.datetime.now()

S, E = range(2)
X, Y, Z = range(3)

def bricks_overlap(a, b):
    return (a[S][X] in range(b[S][X], b[E][X] + 1) or b[S][X] in range(a[S][X], a[E][X] + 1)) and \
           (a[S][Y] in range(b[S][Y], b[E][Y] + 1) or b[S][Y] in range(a[S][Y], a[E][Y] + 1))

bricks = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        start, end = line.split('~')
        bricks.append((list(map(int, start.split(','))), list(map(int, end.split(',')))))

bricks = list(sorted(bricks, key=lambda x: x[S][Z]))

for index, brick in enumerate(bricks):
    delta, top_support = 0, 1
    for support in bricks[:index]:
        if bricks_overlap(brick, support):
            top_support = max(top_support, support[E][Z])
    delta = brick[S][Z] - top_support - 1
    if delta and index:
        brick[E][Z] -= delta
        brick[S][Z] -= delta

bricks = list(sorted(bricks, key=lambda x: x[S][Z]))

supports = defaultdict(set)
supported = defaultdict(set)
for lo, hi in [(lo, hi) for hi in range(len(bricks)) for lo in range(hi)]:
    lo_brick, hi_brick = bricks[lo], bricks[hi]
    if lo_brick[E][Z] + 1 == hi_brick[S][Z] and bricks_overlap(lo_brick, hi_brick):
        supports[lo].add(hi)
        supported[hi].add(lo)

total = 0
for idx in range(len(bricks)):
    if idx not in supports:
        total += 1
    elif all(len(supported[sidx]) > 1 for sidx in supports[idx]):
        total += 1

print(f'part 1: {total}')

total = 0
for lo in range(len(bricks)):
    q = deque(hi for hi in supports[lo] if len(supported[hi]) == 1)
    falling = set(q) | {lo}

    while q:
        current_falling = q.popleft()
        for hi in [hi for hi in supports[current_falling] if hi not in falling and all(s in falling for s in supported[hi])]:
            falling.add(hi)
            q.append(hi)

    total += len(falling) - 1
print(f'part 2: {total}')
print(datetime.datetime.now() - begin_time)
