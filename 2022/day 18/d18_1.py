import datetime

import showgrid
from aopython import vector_add

begin_time = datetime.datetime.now()


def adjacents(p):
    for d in [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]:
        yield tuple(vector_add(p, d))


points = set()
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        points.add(tuple(map(int, line.split(','))))

sides = 0
for p in points:
    sides += sum(map(lambda a: 0 if a in points else 1, adjacents(p)))

showgrid.voxels(points)
print(sides)
print(datetime.datetime.now() - begin_time)
