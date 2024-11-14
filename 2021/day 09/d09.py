import datetime
from collections import deque
from functools import reduce

from aopython import vector_add

begin_time = datetime.datetime.now()
DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))
grid = []


def in_grid(x, y):
    global grid
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)


def bfs(start):
    seen = set()
    q = deque([start])

    while q:
        nx, ny = q.popleft()
        seen.add((nx, ny))

        for d in DIRS:
            px, py = vector_add((nx, ny), d)
            if in_grid(px, py) and grid[ny][nx] < grid[py][px] != 9:
                q.append((px, py))

    return len(seen)


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        grid.append(list(map(int, line)))

lows = []
for x, y, val in [(x, y, val) for y, row in enumerate(grid) for x, val in enumerate(row)]:
    for px, py in [vector_add((x, y), d) for d in DIRS]:
        if in_grid(px, py):
            if grid[py][px] <= val:
                break
    else:
        lows.append((x, y))

print(f'part 1: {sum([1 + grid[y][x] for x, y in lows])}')

basin_sizes = []
for lp in lows:
    basin_sizes.append(bfs(lp))
basin_sizes.sort(reverse=True)
print(f'part 2: {reduce(lambda x, y: x*y, basin_sizes[:3])}')
print(datetime.datetime.now() - begin_time)
