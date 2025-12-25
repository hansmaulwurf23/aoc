import datetime
from itertools import combinations
begin_time = datetime.datetime.now()


def print_points(ps):
    mxx, mxy = max(map(lambda p: p[0], ps)), max(map(lambda p: p[1], ps))
    for y in range(mxy + 1):
        for x in range(mxx + 1):
            if (x, y) in ps:
                print(ps.index((x, y)), end='')
            else:
                print('.', end='')
        print('')


def all_contained(a, b):
    global points
    idx = points.index(a)
    # normalize rect corners with s upper left and e lower right
    sx, sy = (min(a[0], b[0]), min(a[1], b[1]))
    ex, ey = (max(a[0], b[0]), max(a[1], b[1]))

    opx, opy = None, None
    for (px, py) in points[idx:] + points[:idx]:
        # point within
        if (sx < px < ex) and (sy < py < ey):
            return False
        # switched x sides
        if opx is not None and ((opx <= sx and px >= ex) or (opx >= ex and px <= sx)) and sy < py < ey:
            return False
        # switched y sides
        if opy is not None and ((opy <= sy and py >= ey) or (opy >= ey and py <= sy)) and sx < px < ex:
            return False
        opx = px
        opy = py

    return True


points = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        points.append(tuple(map(int, line.split(','))))

# print_points(points)

max_area = None
max_area_contd = None
for a, b in combinations(points, 2):
    contd = all_contained(a, b)
    area = (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
    if contd and (max_area_contd is None or max_area_contd < area):
        max_area_contd = area

    if max_area is None or max_area < area:
        max_area = area

print(f'Part1: {max_area}')
print(f'Part2: {max_area_contd}')
print(datetime.datetime.now() - begin_time)
