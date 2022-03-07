import datetime
import re

from aopython import manhattan_distance, vector_add

begin_time = datetime.datetime.now()

nanobots = dict()
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        x, y, z, range = list(map(int, re.findall(r'-?\d+', line)))
        nanobots[(x, y, z)] = range

in_range_of = dict()
for n in nanobots:
    in_range_of[n] = len([1 for o in nanobots if manhattan_distance(o, n) <= nanobots[o]])

# which nanobot is reached by most others?
max_in_range = max(in_range_of, key=lambda x: in_range_of[x])
# this is the start of the best position
best_pos = tuple(max_in_range)
best_in_range = in_range_of[max_in_range]
print(best_pos, best_in_range)

while True:
    # calc which nanobots are not in range and with which range difference
    not_in_range = dict()
    for n in nanobots:
        if nanobots[n] < (d := manhattan_distance(n, best_pos)):
            not_in_range[n] = abs(d - nanobots[n])

    # which one of these missed the best pos by the least distance
    nearest_miss = min(not_in_range, key=lambda x: not_in_range[x])
    miss_distance = not_in_range[nearest_miss]
    print(f'nearest miss: {nearest_miss} with distance {miss_distance}')

    # move in every dimension the missed distance and calc the then in range nanobots
    new_in_ranges = dict()
    for dim in [(0, 0, miss_distance), (0, miss_distance, 0), (miss_distance, 0, 0)]:
        t = tuple(vector_add(best_pos, dim))
        new_in_ranges[t] = len([1 for o in nanobots if manhattan_distance(o, t) <= nanobots[o]])

    # if moving resulted in more nanobots in range, set the new best pos
    if max(new_in_ranges.values()) > best_in_range:
        best_pos = max(new_in_ranges, key=lambda x: new_in_ranges[x])
        best_in_range = new_in_ranges[best_pos]
        print(f'new best pos {best_pos} to {best_in_range} and distance to origin {manhattan_distance(best_pos, (0, 0, 0))}')
    else:
        print(new_in_ranges)
        break

print(manhattan_distance(best_pos, (0, 0, 0)))
print('32119629 too low')
print('30947521 too low')
print(datetime.datetime.now() - begin_time)
