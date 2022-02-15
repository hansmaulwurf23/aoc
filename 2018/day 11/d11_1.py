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
    grid = dict()
    for y in range(1, GRD_SIZE + 1):
        for x in range(1, GRD_SIZE + 1):
            grid[(x, y)] = calc_cell_power(x, y, serial)
    return grid


def calc_col_sum(grid, x, y):
    return sum([grid[(x, y)], grid[(x, y + 1)], grid[(x, y + 2)]])


def find_max_level(grid):
    max_sum = None
    max_pos = None
    for y in range(1, GRD_SIZE - 2):
        running_col_sum = deque()
        for x in range(1, GRD_SIZE - 2):
            if len(running_col_sum) == 3:
                running_col_sum.popleft()
            running_col_sum.append(calc_col_sum(grid, x, y))
            if len(running_col_sum) == 3:
                cur_sum = sum(running_col_sum)
                if max_sum is None or max_sum < cur_sum:
                    max_sum = cur_sum
                    max_pos = (x-2, y)

    return max_pos


def print_grid(grid):
    for y in range(1, GRD_SIZE + 1):
        for x in range(1, GRD_SIZE + 1):
            print(f'{str(grid[(x, y)]).rjust(3)}', end='')
        print('')


def plot_grid(grid):
    res = []
    for y in range(1, GRD_SIZE + 1):
        row = []
        for x in range(1, GRD_SIZE + 1):
            row.append(grid[(x, y)])
        res.append(row)
    showgrid.pcolormesh(res)


grid = calc_grid(SERIAL)
# print_grid(grid)
plot_grid(grid)
print(find_max_level(grid))
print(datetime.datetime.now() - begin_time)
