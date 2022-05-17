import datetime
import re

from aopython import vector_add

begin_time = datetime.datetime.now()

NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
moves = { NORTH: (0, -1), SOUTH: (0, 1), EAST: (+1, 0), WEST: (-1, 0) }

dir = SOUTH
grid = []

with open('./input.txt') as f:
    while line := f.readline():
        grid.append(line[:])

path = ''

y, x = 0, grid[0].index('|')

while True:
    x, y = vector_add((x, y), moves[dir])
    if re.match('[A-Z]', grid[y][x]):
        path += grid[y][x]
    elif grid[y][x] == '+':
        if dir in (SOUTH, NORTH):
            dir = WEST if grid[y][x-1] == '-' else EAST
        elif dir in (EAST, WEST):
            dir = NORTH if grid[y-1][x] == '|' else SOUTH
    elif grid[y][x] == ' ':
        break

print(path)
print(datetime.datetime.now() - begin_time)
