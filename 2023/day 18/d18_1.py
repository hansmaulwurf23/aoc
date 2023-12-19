import datetime
from collections import deque

from aopython import vector_add

begin_time = datetime.datetime.now()

RIGHT, DOWN, LEFT, UP = range(4)
HEADING = {'L': LEFT, 'R': RIGHT, 'D': DOWN, 'U': UP}
DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def fill(start, fence):
    q = deque([start])
    seen = set()
    fills = 0
    while q:
        pos = q.popleft()

        if pos in seen:
            continue

        seen.add(pos)
        fills += 1

        for npos in [tuple(vector_add(pos, d)) for d in DIRS]:
            if npos not in seen and npos not in fence:
                q.append(npos)

    return fills


cmds = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        dir, amount, color = line.split(' ')
        cmds.append((HEADING[dir], int(amount)))

pos = (0, 0)
grid = set([pos])
for dir, amount in cmds:
    for a in range(amount):
        pos = tuple(vector_add(pos, DIRS[dir]))
        grid.add(pos)

# FIXME: don't guess starting point
p1 = len(grid) + fill((1, 1), grid)
print(f'part 1: {p1}')
assert p1 in [46394, 62]
print(datetime.datetime.now() - begin_time)
