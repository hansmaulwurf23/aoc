import datetime
import re

begin_time = datetime.datetime.now()

SIZE = 1000
grid = []
for y in range(SIZE):
    grid.append([0] * SIZE)

with open('./input.txt') as f:
    while line := f.readline().rstrip():
        toggle = 2
        if line.startswith('turn'):
            toggle = 1 if line[5:7] == 'on' else -1
        fx, fy, tx, ty = map(int, re.findall(r'\d+', line))
        for y in range(fy, ty+1):
            for x in range(fx, tx+1):
                grid[y][x] = max(0, grid[y][x] + toggle)


print(sum(sum(row) for row in grid))
print(datetime.datetime.now() - begin_time)
