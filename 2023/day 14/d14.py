import datetime

from aopython import print_grid

begin_time = datetime.datetime.now()

NORTH, WEST, SOUTH, EAST = range(4)
TRANS = [lambda m: list(zip(*m)),
         lambda m: m,
         lambda m: list(zip(*reversed(m))),
         lambda m: list([list(reversed(l)) for l in m])]

INVERSE = [lambda m: list(zip(*m)),
           lambda m: m,
           lambda m: list(reversed(list(zip(*m)))),
           lambda m: [list(reversed(l)) for l in m]]

def tilt(matrix):
    new_grid, sy = [], len(grid)
    for col in matrix:
        new_col = []
        for part in ''.join(col).split('#'):
            new_part = []
            new_part.extend('O' * part.count('O'))
            new_part.extend('.' * (len(part) - len(new_part)))
            new_part.append('#')
            new_col.extend(new_part)
        new_grid.append(new_col[:-1])

    return new_grid

def calc_weight(grid):
    return sum([row.count('O') * y for y, row in enumerate(reversed(grid), 1)])


def run_cycle(grid):
    for trans, inv in zip(TRANS, INVERSE):
        grid = inv(tilt(trans(grid)))
    return grid

grid = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        grid.append(list(line))

print(f'part 1: {calc_weight(TRANS[NORTH](tilt(TRANS[NORTH](grid))))}')

cycles, cycle = 1_000_000_000, 0
# cycles, cycle = 1_000, 0
# print_grid(grid, sep_below=True)
seen, weights = {}, {}
while True:
    cycle += 1
    grid = run_cycle(grid)

    h = hash(''.join(''.join(l) for l in grid))
    if h in seen:
        cycle_length = cycle - seen[h]
        repeating = (cycles - cycle) // cycle_length
        cycle += repeating * cycle_length

    seen[h] = cycle

    if cycle >= cycles:
        break

print(f'part 2: {calc_weight(grid)}')
print(datetime.datetime.now() - begin_time)
