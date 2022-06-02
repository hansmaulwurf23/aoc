import datetime
from collections import deque

begin_time = datetime.datetime.now()

GRID_W, GRID_H = 50, 6

grid = []
for r in range(GRID_H):
    grid.append([False] * GRID_W)


def rect(grid, args):
    (width, height) = map(int, ' '.join(args).split('x'))
    for y in range(height):
        for x in range(width):
            grid[y][x] = True
    return grid


def rot_row(grid, args):
    row = int(args[1][2:])
    diff = int(args[3])
    new_row = deque(grid[row])
    new_row.rotate(diff)
    grid[row] = list(new_row)
    return grid


def rot_col(grid, args):
    col = int(args[1][2:])
    diff = int(args[3])
    new_row = deque()
    for y in range(len(grid)):
        new_row.append(grid[y][col])
    new_row.rotate(diff)

    for y in range(len(grid)):
        grid[y][col] = new_row[y]

    return grid


def count_lit(grid):
    return sum(map(lambda row: sum(map(lambda x: 1 if x else 0, row)), grid))


def print_grid(grid):
    for row in grid:
        for c in row:
            print(' X ' if c else '   ', end='')
        print('')


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        cmd = line.split()
        if cmd[0] == 'rect':
            rect(grid, cmd[1:])
        elif cmd[0] == 'rotate':
            if cmd[1] == 'column':
                rot_col(grid, cmd[1:])
            elif cmd[1] == 'row':
                rot_row(grid, cmd[1:])

print(print_grid(grid))
print(datetime.datetime.now() - begin_time)
