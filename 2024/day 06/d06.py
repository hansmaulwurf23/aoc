import datetime
from collections import defaultdict

from aopython import vector_add, cmp, vector

begin_time = datetime.datetime.now()

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
INVDIRS = [(0, 1), (-1, 0), (0, -1), (1, 0)]


def is_inside(pos):
    x, y = pos
    return 0 <= x < DIMX and 0 <= y < DIMY


def find_next_obstacle(pos, dir, xob, yob):
    dirobs, dim = (xob, 1) if dir % 2 == 0 else (yob, 0)
    inverse_dim = (dim + 1) % 2
    heading = DIRS[dir][dim]
    obs = list(filter(lambda o: cmp(o, pos[dim]) == heading, dirobs[pos[inverse_dim]]))

    if not obs:
        last_pos = list(pos)
        last_pos[dim] = 0 if heading < 0 else (DIMX if dim == 1 else DIMY) - 1
        steps = abs(sum(vector(last_pos, pos)))
        return None, steps, last_pos

    ob = list(pos)
    ob[dim] = min(obs) if heading > 0 else max(obs)
    steps = abs(sum(vector(ob, pos))) - 1
    last_pos = vector_add(ob, INVDIRS[dir])
    return ob, steps, last_pos


def walk(start, dir, xob, yob):
    curpos = list(start)
    curdir = dir
    turning_points = set()

    ob, steps, last_pos = find_next_obstacle(curpos, curdir, xob, yob)
    step_sum = steps
    while ob is not None:
        curdir = (curdir + 1) % 4
        curpos = tuple(last_pos)
        if steps > 0 and curpos in turning_points:
            return None, True
        turning_points.add(curpos)

        ob, steps, last_pos = find_next_obstacle(curpos, curdir, xob, yob)
        step_sum += steps

    return step_sum, False


obstacles = set()
with open('./input.txt') as f:
    lines = list(map(lambda l: l.rstrip(), f.readlines()))

DIMX, DIMY = len(lines[0]), len(lines)
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == '#':
            obstacles.add((x, y))
        elif c == '^':
            start = (x, y)

xob, yob, pos = defaultdict(list), defaultdict(list), tuple(start)
for x, y in obstacles:
    xob[x].append(y)
    yob[y].append(x)

seen, path, curdir = {pos}, [], 0
path = []
while True:
    nxt_pos = tuple(vector_add(pos, DIRS[curdir]))
    if nxt_pos in obstacles:
        curdir = (curdir + 1) % 4
    else:
        if not is_inside(nxt_pos):
            break
        pos = nxt_pos
        seen.add(pos)
        path.append(pos)
print(f'part 1: {len(seen)}')

ex_pos = {(3, 6), (6, 7), (7, 7), (1, 8), (3, 8), (7, 9)}
new_obs = set()
for px, py in [p for p in path if p not in new_obs]:
    yob[py].append(px)
    xob[px].append(py)
    _, loops = walk(start, 0, xob, yob)
    if loops:
        new_obs.add((px, py))
        # assert (px, py) in ex_pos
    yob[py].remove(px)
    xob[px].remove(py)

print(f'part 2: {len(new_obs)}')
print(datetime.datetime.now() - begin_time)
