import copy
import datetime
from collections import defaultdict

from aopython import vector_add

begin_time = datetime.datetime.now()

FREE, TREE, LUMB = range(3)
symbols = ['.', '|', '#']

grid = []


def in_grid(grid, pos):
    x, y = pos
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


def adjacents(grid, pos):
    res = defaultdict(lambda: 0)
    for d in [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]:
        ax, ay = vector_add(pos, d)
        if in_grid(grid, (ax, ay)):
            res[grid[ay][ax]] += 1

    return res


def step(grid):
    new_grid = copy.deepcopy(grid)
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            vicinity = adjacents(grid, (x, y))
            tile = grid[y][x]
            if tile == FREE:
                if vicinity[TREE] >= 3:
                    new_grid[y][x] = TREE
            elif tile == TREE:
                if vicinity[LUMB] >= 3:
                    new_grid[y][x] = LUMB
            elif tile == LUMB:
                if vicinity[LUMB] >= 1 and vicinity[TREE] >= 1:
                    new_grid[y][x] = LUMB
                else:
                    new_grid[y][x] = FREE

    return new_grid


def resource_value(grid):
    res = defaultdict(lambda: 0)
    for row in grid:
        for v in row:
            res[v] += 1

    return res


def print_grid(grid):
    for row in grid:
        print(''.join(list(map(lambda v: symbols[v], row))))


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        grid.append(list([symbols.index(c) for c in line]))

for minute in range(10):
    grid = step(grid)
    # print_grid(grid)
res_val = resource_value(grid)
print(res_val[TREE] * res_val[LUMB])
print(datetime.datetime.now() - begin_time)
