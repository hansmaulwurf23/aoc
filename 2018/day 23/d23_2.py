import datetime
import re
from z3 import Int, If, Optimize

begin_time = datetime.datetime.now()

nanobots = dict()
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        x, y, z, r = list(map(int, re.findall(r'-?\d+', line)))
        nanobots[(x, y, z)] = r

def zabs(x):
    return If(x >= 0, x, -x)


def with_sum(nanobots):
    x, y, z = Int('x'), Int('y'), Int('z')
    in_ranges = Int('in_ranges')
    range_expr = 0
    for (px, py, pz), r in nanobots.items():
        range_expr += If(zabs(px - x) + zabs(py - y) + zabs(pz - z) <= r, 1, 0)
    o = Optimize()
    o.add(in_ranges == range_expr)
    o.maximize(in_ranges)
    o.minimize(zabs(x) + zabs(y) + zabs(z))
    o.check()

    model = o.model()
    x, y, z = (model[x].as_long(), model[y].as_long(), model[z].as_long())
    return abs(x) + abs(y) + abs(z)


def with_lists(nanobots):
    x, y, z = Int('x'), Int('y'), Int('z')
    in_ranges = [Int(f'in_range_{i}') for i in range(len(nanobots))]
    range_count = Int('sum')
    o = Optimize()

    for i, ((px, py, pz), r) in enumerate(nanobots.items()):
        o.add(in_ranges[i] == If(zabs(x - px) + zabs(y - py) + zabs(z - pz) <= r, 1, 0))

    o.add(range_count == sum(in_ranges))

    manhattan = Int('dist')
    o.add(manhattan == zabs(x) + zabs(y) + zabs(z))
    o.maximize(range_count)
    o.minimize(manhattan)
    o.check()
    return o.model()[manhattan].as_long()


print(with_lists(nanobots))
print(datetime.datetime.now() - begin_time)
