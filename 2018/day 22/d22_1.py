import datetime
import re

begin_time = datetime.datetime.now()
depth = None
target = None
mouth = (0, 0)
geolo_cache = dict()
ROCKY, WET, NARROW = range(3)
ERO, GEO, RISK = range(3)
symbols = {ROCKY: '.', WET: '=', NARROW: '|'}
MAGICMOD = 20183


def build_map(topleft, bottomright):
    sx, sy = topleft
    tx, ty = bottomright
    grid = []
    for y in range(sy, ty + 1):
        grid.append([])
        for x in range(sx, tx + 1):
            if (x, y) == topleft or (x, y) == bottomright:
                geo = 0
            elif y == 0:
                geo = x * 16807
            elif x == 0:
                geo = y * 48271
            else:
                geo = grid[y-1][x][ERO] * grid[y][x - 1][ERO]

            ero = (geo + depth) % MAGICMOD
            risk = ero % 3
            grid[-1].append((ero, geo, risk))

    return grid


def risk_level(grid):
    return sum([sum([v[RISK] for v in row]) for row in grid])


with open('./input.txt') as f:
    lines = f.readlines()
    depth = list(map(int, re.findall(r'\d+', lines[0])))[0]
    target = tuple(map(int, re.findall(r'\d+', lines[1])))

print(risk_level(build_map(mouth, target)))
print(datetime.datetime.now() - begin_time)
