import datetime
from itertools import pairwise
from aopython import vector_add, vector_mul

begin_time = datetime.datetime.now()

RIGHT, DOWN, LEFT, UP = range(4)
VERT, HORIZ = (DOWN, UP), (LEFT, RIGHT)
DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


cmds = []
with open('./test.txt') as f:
    while line := f.readline().rstrip():
        code = line.split(' ')[-1][2:-1]
        amount, dir = int(code[:-1], 16), int(code[-1])
        cmds.append((dir, amount))

# used this to check alternating dimensions
# assert all(v[0] in VERT for v in cmds[1::2)
# assert all(h[0] in HORIZ for h in cmds[::2])
points = [(0,0)]
asum = 0
for dir, amount in cmds:
    asum += amount
    points.append(tuple(vector_add(points[-1], vector_mul(DIRS[dir], amount))))

# https://en.wikipedia.org/wiki/Shoelace_formula
p2 = sum([((x1 - x2) * (y2 + y1)) for (x1, y1), (x2, y2) in pairwise(points)]) // 2
p2 += (asum // 2 + 1)

print(f'part 2: {p2}')
assert p2 in [952408144115, 201398068194715]
print(datetime.datetime.now() - begin_time)
