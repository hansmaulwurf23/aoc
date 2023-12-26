import datetime
from itertools import combinations

begin_time = datetime.datetime.now()

def infer_linear_func(h):
    # y = ax + b
    p, v = h
    a = v[1] / v[0]
    b = p[1] - (p[0] * a)
    return a, b

hailstones = []
with open('./test.txt') as f:
    while line := f.readline().rstrip():
        pos, v = line.split(' @ ')
        hailstones.append([list(map(int, pos.split(', '))), list(map(int, v.split(', ')))])

MIN, MAX = 7, 27
# MIN, MAX = 200000000000000, 400000000000000
tot = 0
for h1, h2 in combinations(hailstones, 2):
    a1, b1 = infer_linear_func(h1)
    a2, b2 = infer_linear_func(h2)

    if a1 == a2:
        if b1 == b2:
            tot += 1
    else:
        x = (b2 - b1) / (a1 - a2)
        y = (a1 * (b2 - b1) / (a1 - a2)) + b1
        t1 = (x - h1[0][0]) / h1[1][0]
        t2 = (x - h2[0][0]) / h2[1][0]
        if t1 > 0 and t2 > 0:
            if MIN <= x <= MAX and MIN <= y <= MAX:
                print(x, y, t1, t2)
                tot += 1
            # else:
                #print('intersect outside', x, y, h1, h2, t1, t2)
        else:
            print('intersect past', x, y, h1, h2, t1, t2)

p1 = tot
print(f'part 1: {p1}')
assert p1 in [19523, 2]
print(datetime.datetime.now() - begin_time)
