import datetime
from collections import deque

import showgrid

begin_time = datetime.datetime.now()
GRD_SIZE = 300
SERIAL = 2866
# SERIAL = 42


def calc_cell_power(x, y, serial):
    return ((((x + 10) * y + serial) * (x + 10)) // 100) % 10 - 5


def calc_grid(serial):
    grid = []
    for y in range(1, GRD_SIZE + 1):
        row = []
        for x in range(1, GRD_SIZE + 1):
            row.append(calc_cell_power(x, y, serial))
        grid.append(row)
    return grid


def calc_row_sum(grid, x, y, size):
    return sum(grid[y][x:x+size])


def find_max_level(grid, size):
    max_sum = None
    max_pos = None
    next_row_running_sum = [None] * GRD_SIZE
    for x in range(GRD_SIZE - size + 1):
        running_row_sum = deque()
        for y in range(GRD_SIZE):
            # make sure we have as much rows as the inspected window
            if len(running_row_sum) == size:
                running_row_sum.popleft()

            # use previously calculated values
            if next_row_running_sum[y] is None:
                running_row_sum.append(calc_row_sum(grid, x, y, size))
            else:
                running_row_sum.append(next_row_running_sum[y] + grid[y][x+size-1])

            next_row_running_sum[y] = (running_row_sum[-1] - grid[y][x])

            if len(running_row_sum) == size:
                cur_sum = sum(running_row_sum)
                if max_sum is None or max_sum < cur_sum:
                    max_sum = cur_sum
                    max_pos = (x + 1, y - size + 2)

    return max_sum, max_pos, size


grid = calc_grid(SERIAL)
levels = []
for s in range(1, GRD_SIZE+1):
    levels.append(find_max_level(grid, s))
max_lvl = max(levels, key=lambda x: x[0])
showgrid.plot_xy(list(map(lambda t: (t[2], t[0]), levels)))
print(max_lvl)
# print(find_max_level(grid, 3))
print(datetime.datetime.now() - begin_time)
