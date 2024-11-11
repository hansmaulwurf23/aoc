import datetime
from aopython import cmp

begin_time = datetime.datetime.now()

field = [[0] * 1000 for i in range(1000)]
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        fx,fy,tx,ty = map(int, line.replace(' -> ',',').split(','))
        dx, dy = cmp(tx, fx), cmp(ty, fy)

        while fx != (tx + dx) or fy != (ty + dy):
            field[fy][fx] += 1
            fx += dx
            fy += dy

print(sum([sum([1 if x > 1 else 0 for x in row]) for row in field]))
print(datetime.datetime.now() - begin_time)
