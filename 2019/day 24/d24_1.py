import datetime
from copy import deepcopy
import showgrid
from aopython import vector_add

begin_time = datetime.datetime.now()
adjacent_deltas = {(0, 1), (0, -1), (+1, 0), (-1, 0)}

size = 5
grid = []
configs = set()

def in_grid(x, y):
    return 0 <= x < size and 0 <= y < size


def plot(grid):
    showgrid.show_grid([(x, -y) for x in range(size) for y in range(size) if grid[y][x]], s=360)


def count_adj_bugs(x, y, grid):
    res = [(ax, ay) for ax, ay in [vector_add(a, (x, y)) for a in adjacent_deltas] if in_grid(ax, ay) and grid[ay][ax]]
    return len(res)


def biodiv(grid):
    sum = 0
    p = 1
    for row in grid:
        for cell in row:
            if cell:
                sum += p
            p = p << 1
    return sum


def cycle(grid):
    new_grid_on_the_block = deepcopy(grid)
    for x, y in [(x, y) for x in range(size) for y in range(size)]:
        adj_bugs = count_adj_bugs(x, y, grid)
        if grid[y][x]:
            new_grid_on_the_block[y][x] = True if adj_bugs == 1 else False
        else:
            new_grid_on_the_block[y][x] = True if 1 <= adj_bugs <= 2 else False

    return new_grid_on_the_block


def run(grid):
    while True:
        # plot(grid)
        grid = cycle(grid)
        if (b := biodiv(grid)) in configs:
            print(b)
            break
        else:
            configs.add(b)


with open('./input.txt') as f:
    y = 0
    while line := f.readline().rstrip():
        grid.append(list(map(lambda x: True if x == '#' else False, line)))

run(grid)
print(datetime.datetime.now() - begin_time)
