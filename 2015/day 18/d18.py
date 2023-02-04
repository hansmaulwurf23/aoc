import datetime
from copy import deepcopy
begin_time = datetime.datetime.now()


def read_initial():
    with open('./input.txt') as f:
        return [list(line.rstrip()) for line in f.readlines()]


def step(grid: list, fixed_edges=False):
    w, h = len(grid[0]), len(grid)
    new_grid = deepcopy(grid)

    for y, row in enumerate(grid):
        # initialize counter for every row
        counter = 0
        if y > 0 and grid[y-1][0] == '#':
            counter += 1
        if y < h - 1 and grid[y+1][0] == '#':
            counter += 1

        for x, c in enumerate(row):
            # enhance running counter to the right
            if x < w - 1:
                if y > 0 and grid[y-1][x+1] == '#':
                    counter += 1
                if grid[y][x+1] == '#':
                    counter += 1
                if y < h - 1 and grid[y+1][x+1] == '#':
                    counter += 1

            # actual game of life
            if c == '#':
                if not 2 <= counter <= 3:
                    new_grid[y][x] = '.'
            else:
                if counter == 3:
                    new_grid[y][x] = '#'

            # reduce left side to prepare for next round
            if x > 0:
                if y > 0 and grid[y-1][x-1] == '#':
                    counter -= 1
                if grid[y][x-1] == '#':
                    counter -= 1
                if y < h - 1 and grid[y+1][x-1] == '#':
                    counter -= 1

            # center now counts as well
            if c == '#':
                counter += 1
            if x < w - 1 and grid[y][x+1] == '#':
                counter -= 1

    if fixed_edges:
        new_grid[0][0] = '#'
        new_grid[h-1][0] = '#'
        new_grid[0][w-1] = '#'
        new_grid[h-1][w-1] = '#'

    return new_grid



initial_grid = read_initial()
g = initial_grid
for s in range(100):
    g = step(g)

print(sum([sum([1 if c == '#' else 0 for c in row]) for row in g]))

g = initial_grid
for s in range(100):
    g = step(g, fixed_edges=True)

print(sum([sum([1 if c == '#' else 0 for c in row]) for row in g]))
print(datetime.datetime.now() - begin_time)
