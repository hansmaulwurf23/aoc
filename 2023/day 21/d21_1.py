import datetime
from collections import deque
from aopython import vector_add, divisors

begin_time = datetime.datetime.now()

N, E, S, W = range(4)
DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))

def in_grid(pos):
    global grid, infinite
    if infinite:
        return True
    x, y = pos
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)

def is_plot(pos):
    global grid, infinite
    x, y = pos
    w, h = len(grid[0]), len(grid)
    if infinite:
        return grid[y % HEIGHT][x % WIDTH] != '#'
    else:
        return grid[y][x] != '#'

def adjacents(pos):
    global grid
    return [pos for pos in [tuple(vector_add(d, pos)) for d in DIRS] if in_grid(pos) and is_plot(pos)]

def print_grid(seen, start):
    global grid
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if (x, y) in seen:
                print('O', end='')
            elif (x, y) == start:
                print('S', end='')
            else:
                print(grid[y][x], end='')
        print('')

def bfs(start, max_steps):
    valids = set()
    seen = {start}
    q = deque([(max_steps, start)])

    while q:
        steps, pos = q.popleft()

        if steps % 2 == 0:
            valids.add(pos)

        for a in adjacents(pos):
            if a not in seen and steps:
                seen.add(a)
                q.append((steps - 1, a))

    return len(valids)


with open('./input.txt') as f:
    grid = [list(line) for line in f.read().splitlines()]

WIDTH, HEIGHT = len(grid[0]), len(grid)
for y, line in enumerate(grid):
    for x, c in enumerate(line):
        if c == 'S':
            start = (x, y)

infinite = False
valids = bfs(start, 64)
print(f'part 1: {valids}')
assert valids in (3858, 16)

print(datetime.datetime.now() - begin_time)
