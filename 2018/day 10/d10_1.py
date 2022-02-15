import datetime
import re

import showgrid
from aopython import min_max_2d

begin_time = datetime.datetime.now()

def calc_sim_pos(flares, steps):
    res = []
    for x, y, vx, vy in flares:
        res.append((x + steps * vx, y + steps * vy))

    return res


def calc_flares_area(positions):
    fx, tx, fy, ty = min_max_2d(positions)
    return [tx - fx, ty - fy]


def run_to_min_area(flares):
    x_size, y_size = calc_flares_area(flares)
    max_vx = max(map(lambda v: abs(v), [v[2] for v in flares]))
    max_vy = max(map(lambda v: abs(v), [v[3] for v in flares]))
    # roughly estimate coming from both sides and 100 steps margin
    steps = min([x_size // max_vx, y_size // max_vy]) // 2 - 100
    last_area = None
    while True:
        steps += 1
        area = calc_flares_area(calc_sim_pos(flares, steps))
        if last_area is not None and last_area < area:
            return steps - 1
        else:
            last_area = area


def print_flares(flares, steps):
    positions = calc_sim_pos(flares, steps)
    fx, tx, fy, ty = min_max_2d(positions)
    for y in range(fy, ty + 1):
        for x in range(fx, tx + 1):
            print(f"{'#' if (x, y) in positions else ' '}", end='')
        print('')


flares = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        flares.append(list(map(int, re.findall(r'-?\d+', line))))

sim_steps = run_to_min_area(flares)
print_flares(flares, sim_steps)
print(datetime.datetime.now() - begin_time)
