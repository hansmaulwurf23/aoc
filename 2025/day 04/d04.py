import datetime

from aopython import vector_add

begin_time = datetime.datetime.now()

DIRS = tuple((x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if x != 0 or y != 0)
PAPER, REMOVED = '@', 'x'


def in_grid(x, y):
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)


def grid_val(x, y):
    return grid[y][x]


def count_adjs(pos):
    return sum([grid_val(*np) == PAPER for np in [vector_add(pos, d) for d in DIRS] if in_grid(*np)])


grid = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        grid.append(list(line))

part1 = 0
removals = set()
for y, row in enumerate(grid):
    for x, val in [(x, v) for x, v in enumerate(row) if v == PAPER]:
        if count_adjs((x, y)) < 4:
            part1 += 1
            removals.add((x, y))

part2 = 0
while removals:
    pos = removals.pop()
    part2 += 1
    x, y = pos
    grid[y][x] = REMOVED
    for np in [np for np in [vector_add(pos, d) for d in DIRS] if in_grid(*np) and grid_val(*np) == PAPER]:
        if count_adjs(np) < 4:
            removals.add(tuple(np))

print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
assert part1 in (1356, 13)
print(datetime.datetime.now() - begin_time)
