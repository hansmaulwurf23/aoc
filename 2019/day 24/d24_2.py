import datetime
from copy import deepcopy
import showgrid
from aopython import vector_add

begin_time = datetime.datetime.now()
adjacent_deltas = {(0, 1), (0, -1), (+1, 0), (-1, 0)}

size = 5
grids = dict()
configs = set()


def print_grids(grids):
    for lvl in sorted(grids.keys()):
        print(f'\n{lvl}')
        for y, row in enumerate(grids[lvl]):
            for x, cell in enumerate(row):
                if (x, y) == (2, 2):
                    print('?', end='')
                else:
                    print(f"{'#' if cell else '.'}", end='')
            print('')


def in_level_grid(x, y, lvl, grids):
    return 0 <= x < size and 0 <= y < size and lvl in grids.keys() and (x, y) != (2, 2)


# FIXME count here directly instead of collecting coordinates first
def count_adj_bugs(x, y, lvl, grids):
    adjacents = []
    for (ax, ay) in [vector_add(a, (x, y)) for a in adjacent_deltas]:
        if in_level_grid(ax, ay, lvl, grids):
            adjacents.append((ax, ay, lvl))
        elif (ax, ay) == (2, 2) and (lvl + 1) in grids.keys():
            if x == 1:
                adjacents.extend([(0, ly, lvl + 1) for ly in range(size)])
            if x == 3:
                adjacents.extend([(4, ly, lvl + 1) for ly in range(size)])
            if y == 1:
                adjacents.extend([(lx, 0, lvl + 1) for lx in range(size)])
            if y == 3:
                adjacents.extend([(lx, 4, lvl + 1) for lx in range(size)])
        elif (lvl - 1) in grids.keys():
            if ax == -1:
                adjacents.append((1, 2, lvl - 1))
            if ay == -1:
                adjacents.append((2, 1, lvl - 1))
            if ax == size:
                adjacents.append((3, 2, lvl - 1))
            if ay == size:
                adjacents.append((2, 3, lvl - 1))

    # if len(adjacents) == 8:
    #     print(f'({x},{y},{z}) has {len(adjacents)} adjacents')
    return len([1 for (ax, ay, az) in adjacents if grids[az][ay][ax]])


def count_all_bugs(grids):
    return sum(sum(sum(1 if cell else 0 for cell in row) for row in grid) for grid in grids.values())


def count_grid_bugs(grid):
    return sum(sum(1 if cell else 0 for cell in row) for row in grid)


def gen_new_grid():
    new_grid = []
    for row in range(size):
        new_grid.append([False] * size)

    return new_grid


def cycle_grid(grids, lvl):
    new_grid = gen_new_grid()
    for x, y in [(x, y) for x in range(size) for y in range(size) if (x, y) != (2, 2)]:
        adj_bugs = count_adj_bugs(x, y, lvl, grids)
        if lvl in grids.keys() and grids[lvl][y][x]:
            new_grid[y][x] = True if adj_bugs == 1 else False
        else:
            new_grid[y][x] = True if 1 <= adj_bugs <= 2 else False

    return new_grid


def cycle(grids):
    new_grids_on_the_block = dict()
    for lvl, grid in grids.items():
        new_grids_on_the_block[lvl] = cycle_grid(grids, lvl)

    # only extend the recursion levels down and upward if the current min and max levels contain bugs (half exec time!)
    min_lvl = min(grids.keys())
    if count_grid_bugs(new_grids_on_the_block[min_lvl]):
        new_grids_on_the_block[min_lvl - 1] = cycle_grid(grids, min_lvl - 1)
    max_lvl = max(grids.keys())
    if count_grid_bugs(new_grids_on_the_block[max_lvl]):
        new_grids_on_the_block[max_lvl + 1] = cycle_grid(grids, max_lvl + 1)
    return new_grids_on_the_block


def run(grids):
    for age in range(1, 201):
        grids = cycle(grids)

    print(f'minute {age} level: {len(grids)} bugs: {count_all_bugs(grids)}')


with open('./input.txt') as f:
    grids[0] = []
    while line := f.readline().rstrip():
        grids[0].append(list(map(lambda x: True if x == '#' else False, line)))

run(grids)
print(datetime.datetime.now() - begin_time)
