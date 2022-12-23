import datetime
import os
from collections import defaultdict
import imageio as imageio
import showgrid
from aopython import vector_add

begin_time = datetime.datetime.now()

#  7 0 1
#  6 X 2
#  5 4 3
N, NE, E, SE, S, SW, W, NW = range(8)
MOVES = {N: (0, 1), NE: (1, 1), E: (1, 0), SE: (1, -1), S: (0, -1), SW: (-1, -1), W: (-1, 0), NW: (-1, 1)}
# hard coding this? yes, because fiddle this fuck in code is not readable thats why
CHECK_PRIO = [((N, NW, NE), (S, SE, SW), (W, NW, SW), (E, NE, SE)),
              ((S, SE, SW), (W, NW, SW), (E, NE, SE), (N, NW, NE)),
              ((W, NW, SW), (E, NE, SE), (N, NW, NE), (S, SE, SW)),
              ((E, NE, SE), (N, NW, NE), (S, SE, SW), (W, NW, SW))]

elves, no_elves, cur_prio = set(), None, 0


def round(elves, cur_prio):
    prop_moves = defaultdict(list)
    new_elves = set()

    for e in elves:
        moved = False
        free_dirs = [tuple(vector_add(e, MOVES[d])) not in elves for d in range(len(MOVES))]
        if all(free_dirs):
            prop_moves[e].append(e)
            continue
        for checks in CHECK_PRIO[cur_prio]:
            direction = checks[0]
            if all(free_dirs[check] for check in checks):
                np = tuple(vector_add(e, MOVES[direction]))
                prop_moves[np].append(e)
                moved = True
                break
        if not moved:
            # is that even right?
            prop_moves[e].append(e)

    for np, movers in prop_moves.items():
        if len(movers) == 1:
            new_elves.add(np)
        else:
            new_elves |= set(movers)

    return new_elves


def calc_free_ground(elves):
    minx, maxx, miny, maxy = [None] * 4
    for ex, ey in elves:
        if minx is None or ex < minx: minx = ex
        if maxx is None or ex > maxx: maxx = ex
        if miny is None or ey < miny: miny = ey
        if maxy is None or ey > maxy: maxy = ey

    return (maxx - minx + 1) * (maxy - miny + 1) - no_elves


with open('./input.txt') as f:
    y = 0
    while line := f.readline().rstrip():
        for x, c in enumerate(line):
            if c == '#':
                elves.add((x, y))
        y -= 1

    no_elves = len(elves)


for r in range(10):
    # showgrid.show_grid(elves)
    elves = round(elves, cur_prio)
    cur_prio = (cur_prio + 1) % len(CHECK_PRIO)

# showgrid.show_grid(elves, s=8)
print(calc_free_ground(elves))
print(datetime.datetime.now() - begin_time)

