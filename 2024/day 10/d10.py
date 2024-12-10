import datetime
from collections import deque
from aopython import vector_add

begin_time = datetime.datetime.now()
DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))

def in_grid(y, x):
    global DIMX, DIMY
    return 0 <= x < DIMX and 0 <= y < DIMY

def height(y, x):
    global grid
    return int(grid[y][x]) if in_grid(y, x) and grid[y][x] != '.' else None

def bfs(start, ignore_seen = False):
    q = deque([start])
    seen, ends = set(), 0

    while q:
        cur = q.popleft()
        cur_height = height(*cur)

        if cur_height == 9:
            ends += 1
            continue

        for nxt in [tuple(vector_add(cur, d)) for d in DIRS]:
            if (nxt not in seen or ignore_seen) and height(*nxt) == cur_height + 1:
                q.append(nxt)
                seen.add(nxt)

    return ends


trailheads = []
with open('./input.txt') as f:
    grid = list(map(lambda l: l.rstrip(), f.readlines()))
    DIMX, DIMY = len(grid[0]), len(grid)
    for x, y, c in [(x, y, c) for y, l in enumerate(grid) for x, c in enumerate(l) if c == '0']:
        trailheads.append((y, x))


sum1, sum2 = 0, 0
for t in trailheads:
    sum1 += bfs(t)
    sum2 += bfs(t, ignore_seen = True)

print(f'part 1: {sum1}')
print(f'part 2: {sum2}')
print(datetime.datetime.now() - begin_time)
