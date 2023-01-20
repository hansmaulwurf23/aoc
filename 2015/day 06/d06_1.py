import datetime
import re

begin_time = datetime.datetime.now()

SIZE = 1000
grid = []
for y in range(SIZE):
    grid.append([False] * SIZE)

with open('./input.txt') as f:
    while line := f.readline().rstrip():
        toggle = None
        if line.startswith('turn'):
            toggle = line[5:7] == 'on'
        fx, fy, tx, ty = map(int, re.findall(r'\d+', line))
        for y in range(fy, ty+1):
            for x in range(fx, tx+1):
                grid[y][x] = toggle if toggle is not None else not grid[y][x]


print(sum(sum(row) for row in grid))
print(datetime.datetime.now() - begin_time)
