import datetime
import re

from aopython import manhattan_distance

begin_time = datetime.datetime.now()

nanobots = dict()
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        x, y, z, range = list(map(int, re.findall(r'-?\d+', line)))
        nanobots[(x, y, z)] = range

in_range_of = dict()
for n in nanobots:
    in_range_of[n] = len([1 for o in nanobots if manhattan_distance(o, n) <= nanobots[o]])

max_in_range = max(in_range_of, key=lambda x: in_range_of[x])
print(max_in_range, in_range_of[max_in_range])
best_pos = tuple(max_in_range)
not_in_max_range = dict()
for n in nanobots:
    if nanobots[n] < (d := manhattan_distance(n, max_in_range)):
        not_in_max_range[n] = abs(d - nanobots[n])

nearest_miss = min(not_in_max_range, key=lambda x: not_in_max_range[x])
print(nearest_miss, not_in_max_range[nearest_miss])
print(manhattan_distance(best_pos, (0, 0, 0)))
print('30947521 too low')
print(datetime.datetime.now() - begin_time)
