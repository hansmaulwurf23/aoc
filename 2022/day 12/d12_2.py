import datetime
from collections import deque

import showgrid
from aopython import vector_add

begin_time = datetime.datetime.now()

grid = []
cur = (0, 0)
dst = (0, 0)


def bfs(root):
    q = deque()
    q.append((root, 0))
    seen = set()
    while True:
        cur_pos, steps = q.popleft()
        if cur_pos in seen:
            continue

        if grid[cur_pos[1]][cur_pos[0]] == 0:
            return steps

        seen.add(cur_pos)

        for a in adjacents(*cur_pos):
            if a not in seen:
                q.append((a, steps + 1))


def adjacents(ox, oy):
    for m in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
        nx, ny = vector_add((ox, oy), m)
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and \
           grid[ny][nx] >= grid[oy][ox] - 1:
            yield tuple([nx, ny])


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        if 'S' in line:
            cur = (line.index('S'), len(grid))
            line = line.replace('S', 'a')
        if 'E' in line:
            dst = (line.index('E'), len(grid))
            line = line.replace('E', 'z')
        grid.append(list(map(lambda c: ord(c) - ord('a'), line)))

print(bfs(dst))
print(datetime.datetime.now() - begin_time)
