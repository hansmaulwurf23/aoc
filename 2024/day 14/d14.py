import datetime
from functools import reduce

from aopython import vector_add

begin_time = datetime.datetime.now()
DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))


def plot_guards(guards):
    global DIMY, DIMX
    for y in range(DIMY):
        for x in range(DIMX):
            print('#' if (x, y) in guards else ' ', end='', flush=True)
        print('')


def count_guards_with_neighbors(guards):
    global DIMY, DIMX
    counter = 0
    for g in guards:
        if next((d for d in DIRS if tuple(vector_add(d, g)) in guards), False):
            counter += 1

    return counter


TMAX = 100
guards = []
DIMX, DIMY, fname = 101, 103, './input.txt'
# DIMX, DIMY, fname = 11, 7, './example.txt'
MIDX, MIDY = DIMX // 2, DIMY // 2
with open(fname) as f:
    while line := f.readline().rstrip():
        p, v = list(map(lambda l: tuple(map(int, l[2:].split(','))), line.split()))
        guards.append((p, v))

counts = [0, 0, 0, 0]
for (px, py), (vx, vy) in guards:
    x = (px + (TMAX * vx)) % DIMX
    y = (py + (TMAX * vy)) % DIMY
    if y != MIDY and x != MIDX:
        counts[(y > MIDY) * 2 + (x > MIDX)] += 1

print(f'part 1: {reduce(lambda a, b: a * b, counts)}')

step = 1
while True:
    new_pos = set()
    for (px, py), (vx, vy) in guards:
        x = (px + (step * vx)) % DIMX
        y = (py + (step * vy)) % DIMY
        new_pos.add((x, y))
    # print(guards_with_neighbors(new_pos))
    if len(new_pos) == len(guards):
        # plot_guards(new_pos)
        break
    step += 1
print(f'part 2: {step}')

print(datetime.datetime.now() - begin_time)
