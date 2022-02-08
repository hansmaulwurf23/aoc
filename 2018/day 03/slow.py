import datetime
from collections import defaultdict, Counter
from functools import reduce

from aopython import vector_add
from collections import namedtuple

Rectangle = namedtuple('Rectangle', 'fx tx fy ty')

begin_time = datetime.datetime.now()

claims = []
X, Y = 0, 1
SW, NE = 0, 1


def parse_info(line):
    id, rest = line.split(' @ ')
    id = id.replace('#', '')
    sw, rest = rest.split(': ')
    sw = list(map(int, sw.split(',')))
    rest = list(map(int, rest.split('x')))
    ne = vector_add(sw, rest)

    return id, Rectangle(sw[0], ne[0], sw[1], ne[1])


def contains(a, b):
    return a.fx <= b.fx and a.tx >= b.tx and a.fy <= b.fy and a.ty >= b.ty


def intersects(a, b):
    return a.fx <= b.tx and a.tx >= b.fx and a.fy <= b.ty and a.ty >= b.fy


def merge_rects(rects):
    if len(rects) <= 1:
        return rects

    x_s = Counter(map(lambda r: tuple(r[0:2]), rects)).most_common(1)[0]
    y_s = Counter(map(lambda r: tuple(r[2:4]), rects)).most_common(1)[0]

    if x_s[1] < y_s[1]:
        mergable = [r for r in rects if r[2:4] == y_s[0]]
        new_rect = Rectangle(min(map(lambda r: r[0], mergable)), max(map(lambda r: r[1], mergable)), *y_s[0])
    else:
        mergable = [r for r in rects if r[0:2] == x_s[0]]
        new_rect = Rectangle(*x_s[0], min(map(lambda r: r[2], mergable)), max(map(lambda r: r[3], mergable)))

    for m in mergable:
        rects.remove(m)
    rects.append(new_rect)

    return rects


def intersection_claims(ex, rect):
    if contains(rect, ex):
        return [], rect

    if not intersects(ex, rect):
        return [ex], None

    new_rects = []
    x_coords = list(sorted([ex.fx, rect.fx, ex.tx, rect.tx]))
    y_coords = list(sorted([ex.fy, rect.fy, ex.ty, rect.ty]))
    for x in range(0, len(x_coords) - 1):
        for y in range(0, len(y_coords) - 1):
            new_rects.append(Rectangle(x_coords[x], x_coords[x + 1], y_coords[y], y_coords[y + 1]))

    intersection = list(filter(lambda r: contains(rect, r) and contains(ex, r), new_rects))[0]
    new_rects.remove(intersection)
    merged_rects = merge_rects(list(filter(lambda r: contains(rect, r), new_rects)))
    merged_rects.extend(merge_rects(list(filter(lambda r: contains(ex, r), new_rects))))
    return merged_rects, intersection


def process_claim(c, processed_claims):
    new_proc_claims = []
    for p in processed_claims:
        rects, intersection = intersection_claims(p, c)
        new_proc_claims.extend(rects)

    new_proc_claims.append(c)
    return new_proc_claims


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        id, rect = parse_info(line)
        claims.append(rect)

claims = list(sorted(claims))
processed_claims = []
print(f'no of claims: {len(claims)}')
for i, c in enumerate(claims):
    print(i, len(processed_claims))
    processed_claims = process_claim(c, processed_claims)

print(processed_claims)
print(datetime.datetime.now() - begin_time)
