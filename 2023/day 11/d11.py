import datetime
from collections import deque
from itertools import combinations
from aopython import manhattan_distance

begin_time = datetime.datetime.now()


def find_expansions(grid):
    rows, cols = [], []
    for y, l in enumerate(grid):
        if all([c == '.' for c in l]):
            rows.append(y)

    for x, c in enumerate(grid[0]):
        if all([l[x] == '.' for l in grid]):
            cols.append(x)

    return rows, cols


def find_galaxies(grid):
    return [(x, y) for y, l in enumerate(grid) for x, c in enumerate(l) if c == '#']


def expand_galaxies(galaxies, erows, ecols, expansion=2):
    return [(x + sum([(expansion - 1) for e in ecols if x > e]),
             y + sum([(expansion - 1) for e in erows if y > e])) for x, y in galaxies]

def find_galaxies_expanded(grid, erows, ecols, expansion=2):
    galaxies = []

    xmap = { x: x + sum([(expansion - 1) for e in ecols if x > e]) for x in range(len(grid[0])) }

    ystretch = 0
    yleft = deque(sorted(erows))
    for y, line in enumerate(grid):
        if yleft and y == yleft[0]:
            ystretch += (expansion - 1)
            yleft.popleft()

        for x, c in enumerate(line):
            if c == '#':
                galaxies.append((xmap[x], y + ystretch))

    return galaxies


with open('./input.txt') as f:
    universe = f.read().splitlines()

erows, ecols = find_expansions(universe)
galaxies = find_galaxies(universe)
print(f'part 1: {sum([manhattan_distance(a, b) for a, b in combinations(expand_galaxies(galaxies, erows, ecols), 2)])}')
print(f'part 2: {sum([manhattan_distance(a, b) for a, b in combinations(expand_galaxies(galaxies, erows, ecols, 1_000_000), 2)])}')
print(datetime.datetime.now() - begin_time)
