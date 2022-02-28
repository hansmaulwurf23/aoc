import datetime
import math

from aopython import vector_add

begin_time = datetime.datetime.now()

NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
turn_left = (WEST, NORTH, EAST, SOUTH)
moves = { NORTH: (0, 1), SOUTH: (0, -1), EAST: (+1, 0), WEST: (-1, 0) }
left_adj = (moves[WEST], moves[NORTH], moves[EAST], moves[SOUTH])


def adjacent_sum(pos, grid):
    sum = 0
    for d in [(1,1), (1,0), (1,-1), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1)]:
        if (dpos := tuple(vector_add(pos, d))) in grid:
            sum += grid[dpos]
    return sum


def build_grid(max_val):
    grid = dict()
    cur_pos = (0, 0)
    cur_dir = EAST
    grid[cur_pos] = 1

    while grid[cur_pos] < max_val:
        cur_pos = tuple(vector_add(cur_pos, moves[cur_dir]))
        grid[cur_pos] = adjacent_sum(cur_pos, grid)

        if tuple(vector_add(cur_pos, left_adj[cur_dir])) not in grid:
            cur_dir = turn_left[cur_dir]

    return adjacent_sum(cur_pos, grid)


print(build_grid(312051))
print('312488 <')
print(datetime.datetime.now() - begin_time)
