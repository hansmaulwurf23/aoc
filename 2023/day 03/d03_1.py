import datetime
from collections import deque
from aopython import vector_add

begin_time = datetime.datetime.now()


def digit_adjacents(grid, pos):
    for d in [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]:
        ax, ay = vector_add(pos, d)
        if '0' <= grid[ay][ax] <= '9':
            yield ax, ay


def digit_pos(grid, pos):
    x, y = pos
    while x >= 0 and '0' <= grid[y][x] <= '9':
        x -= 1

    return x + 1, y


def read_number(grid, pos):
    digits = deque()
    x, y = pos
    while x < len(grid[y]) and '0' <= grid[y][x] <= '9':
        digits.append(grid[y][x])
        x += 1

    return int(''.join(digits))


engine = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        engine.append(list(line))

found = set()
no_sum = 0
for y, row in enumerate(engine):
    for x, c in enumerate(row):
        if c != '.' and not c.isdigit():
            for ap in digit_adjacents(engine, (x, y)):
                dp = digit_pos(engine, ap)
                if dp not in found:
                    no_sum += read_number(engine, dp)
                    found.add(dp)

print(no_sum)
print(datetime.datetime.now() - begin_time)
