import copy
import datetime
from collections import defaultdict, Counter

from aopython import vector_add

begin_time = datetime.datetime.now()

FREE, TREE, LUMB = range(3)
symbols = ['.', '|', '#']

grid = []
adj_cache = dict()


def in_grid(grid, pos):
    x, y = pos
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


def adjacents(grid, pos):
    if pos in adj_cache:
        return adj_cache[pos]

    res = []
    for d in [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]:
        ax, ay = vector_add(pos, d)
        if in_grid(grid, (ax, ay)):
            res.append((ax, ay))

    adj_cache[pos] = res
    return res


def calc_vicinity(adjacents):
    return Counter([grid[ay][ax] for (ax, ay) in adjacents])


def step(grid):
    new_grid = copy.deepcopy(grid)
    res_val = defaultdict(lambda: 0)
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            vicinity = calc_vicinity(adjacents(grid, (x, y)))
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

            res_val[new_grid[y][x]] += 1

    return new_grid, res_val


def resource_value(grid):
    res = defaultdict(lambda: 0)
    for row in grid:
        for v in row:
            res[v] += 1

    return res


def hash_grid_state(dd):
    return '_'.join([f'{v}:{c}' for (v, c) in dd.items()])


def print_grid(grid):
    for row in grid:
        print(''.join(list(map(lambda v: symbols[v], row))))


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        grid.append(list([symbols.index(c) for c in line]))

minutes_left = 1000000000
seen = {hash_grid_state(resource_value(grid))}
first_repeat = None
last_repeat = None
cycle_len = None
while minutes_left:
    minutes_left -= 1
    grid, res_val = step(grid)
    res_hash = hash_grid_state(res_val)
    if cycle_len is None and res_hash in seen:
        if last_repeat is None:
            last_repeat = minutes_left
            first_repeat = minutes_left
            seen_seen = { res_hash }
        elif last_repeat - 1 == minutes_left:
            if res_hash in seen_seen:
                cycle_len = first_repeat - minutes_left
                print(f'cycle length: {cycle_len}')
                minutes_left = minutes_left % cycle_len
            else:
                last_repeat = minutes_left
                seen_seen.add(res_hash)
        else:
            print(f'skipping repeat at {minutes_left} after {first_repeat - minutes_left}')
            last_repeat = None
    else:
        seen.add(res_hash)

print(res_val[TREE] * res_val[LUMB])
print('169234 !')
print(datetime.datetime.now() - begin_time)
