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
    for x in range(GRD_SIZE - size):
        running_row_sum = deque()
        for y in range(GRD_SIZE - size):
            if len(running_row_sum) == size:
                running_row_sum.popleft()
            running_row_sum.append(calc_row_sum(grid, x, y, size))
            if len(running_row_sum) == size:
                cur_sum = sum(running_row_sum)
                if max_sum is None or max_sum < cur_sum:
                    max_sum = cur_sum
                    max_pos = (x + 1, y - size + 2)

    return max_sum, max_pos, size


grid = calc_grid(SERIAL)
# levels = []
# for s in range(1, GRD_SIZE+1):
#     levels.append(find_max_level(grid, s))
# print(levels)
print(find_max_level(grid, 151))
print(datetime.datetime.now() - begin_time)
