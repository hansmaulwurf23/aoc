import datetime
import math
from collections import defaultdict
from itertools import product
from aopython import triangular_number

begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    (lo_x, hi_x), (hi_y, lo_y) = map(lambda x: list(map(int, x[2:].split('..'))),
                                     f.readline().rstrip().replace('target area: ', '').split(', '))

# calc possible x range
minx = math.floor(pow(lo_x * 2, .5)) - 1
valid_x = defaultdict(lambda: [None, None])
while triangular_number(minx) < lo_x:
    minx += 1

for x in range(minx, hi_x + 1):
    px, vx, steps = 0, x, 0
    while px < lo_x and vx:
        px, vx, steps = px + vx, vx - 1, steps + 1

    # in target area
    while lo_x <= px <= hi_x:
        # save minimum steps to reach target area
        if valid_x[x][0] is None: valid_x[x][0] = steps
        valid_x[x][1] = steps
        px, vx, steps = px + vx, vx - 1, steps + 1
        if vx < 0:
            # inside target area but no more x movement (no upper boundary)
            valid_x[x][1] = math.inf
            break

valid_y = defaultdict(lambda: [None, None])
for y in range(0, hi_y - 1, -1):
    py, vy, steps = 0, y, 0
    symmetric_offset, sym_y = 1 + abs(y + 1) * 2, abs(y) - 1
    while py > lo_y:
        py, vy, steps = py + vy, vy - 1, steps + 1

    while lo_y >= py >= hi_y:
        # save minimum steps to reach target area
        if valid_y[y][0] is None: valid_y[y][0] = steps
        if y and valid_y[sym_y][0] is None: valid_y[sym_y][0] = steps + symmetric_offset
        valid_y[y][1] = steps
        valid_y[sym_y][1] = steps + symmetric_offset
        py, vy, steps = py + vy, vy - 1, steps + 1

valid_counter = 0
for vx, vy in product(valid_x, valid_y):
    (fxs, txs), (fys, tys) = valid_x[vx], valid_y[vy]
    if fxs <= fys <= txs or fys <= fxs <= tys:
        valid_counter += 1

# max negative y is the fastest y velocity -> highest point
print(f'part 1: {triangular_number(abs(min(valid_y.keys()) + 1))}')
print(f'part 2: {valid_counter}')
print(datetime.datetime.now() - begin_time)
