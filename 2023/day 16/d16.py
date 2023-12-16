import datetime

from aopython import vector_add

begin_time = datetime.datetime.now()

LEFT, RIGHT, DOWN, UP = range(4)
DIRS = [(-1, 0), (1, 0), (0, 1), (0, -1)]
REFL = {'/':  {RIGHT: UP, LEFT: DOWN, DOWN: LEFT, UP: RIGHT},
        '\\': {RIGHT: DOWN, LEFT: UP, DOWN: RIGHT, UP: LEFT}}
SPLI = {'|': {RIGHT: (DOWN, UP), LEFT: (DOWN, UP)},
        '-': {UP: (LEFT, RIGHT), DOWN: (LEFT, RIGHT)}}
ICON = {LEFT: '<', RIGHT: '>', DOWN: 'v', UP: '^'}
OPPO = {LEFT: RIGHT, RIGHT: LEFT, UP: DOWN, DOWN: UP}

def in_grid(x, y, grid):
    return 0 <= y < len(grid) and 0 <= x < len(grid[y])

def run_beam(pos, dir):
    beams = [[pos, dir]]
    seen = set()
    while beams:
        left_beams = []
        for bpos, bdir in beams:
            bpos = tuple(vector_add(bpos, DIRS[bdir]))
            bx, by = bpos

            if not in_grid(bx, by, grid):
                continue

            if (bpos, bdir) in seen:
                continue
            seen.add((bpos, bdir))

            g = grid[by][bx]
            if g == '.':
                left_beams.append([bpos, bdir])
            elif g in REFL:
                left_beams.append([bpos, REFL[g][bdir]])
            elif g in SPLI:
                if bdir in SPLI[g]:
                    for ndir in SPLI[g][bdir]:
                        left_beams.append([bpos, ndir])
                else:
                    left_beams.append([bpos, bdir])
        beams = left_beams

    return len(set([s[0] for s in seen]))

def print_seen(seen, grid):
    positions = {}
    for spos, sdir in seen:
        if spos in positions:
            if positions[spos] in ICON.values():
                positions[spos] = '2'
            else:
                positions[spos] = str(int(positions[spos]) + 1)
        else:
            positions[spos] = ICON[sdir]

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            print(positions[(x, y)] if (x, y) in positions else '.', end='')
        print('')

with open('./input.txt') as f:
    grid = [list(l) for l in f.read().splitlines()]

p1 = run_beam((-1, 0), RIGHT)
assert p1 in [46, 7199]
print(f'part 1: {p1}')

max_energy = 0
ITER = {RIGHT: DOWN, LEFT: DOWN, DOWN: RIGHT, UP: RIGHT}
STRT = {RIGHT: (-1, 0), LEFT: (len(grid[0]), 0), DOWN: (0, -1), UP: (0, len(grid))}
END =  {RIGHT: (-1, len(grid)), LEFT: (len(grid[0]), len(grid)), DOWN: (len(grid[0]), -1), UP: (len(grid[0]), len(grid))}
for dir in range(4):
    pos = STRT[dir]
    end = END[dir]
    dlt = DIRS[ITER[dir]]
    while pos != end:
        # print(f'{pos} {ICON[dir]}')
        max_energy = max(max_energy, run_beam(pos, dir))
        pos = tuple(vector_add(pos, dlt))

p2 = max_energy
print(f'part 2: {max_energy}')
assert p2 in [51, 7438]
print(datetime.datetime.now() - begin_time)
