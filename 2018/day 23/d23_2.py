import datetime
import re
from collections import deque, defaultdict

from aopython import manhattan_distance, vector_add, vector

begin_time = datetime.datetime.now()


def scalprod(v, s):
    return [d * s for d in v]

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
# print(best_pos, best_in_range)
print(f'new best pos: {best_pos} to {best_in_range} and distance to origin {manhattan_distance(best_pos, (0, 0, 0))}')

q = deque()
q.append((best_pos, best_in_range))
in_range_positions = defaultdict(set)
seen = set()
while q:
    cur_pos, cur_in_range = q.popleft()
    if cur_pos in seen:
        continue
    # calc which nanobots are not in range and with which range difference
    not_in_range = dict()
    for n in nanobots:
        if nanobots[n] < (d := manhattan_distance(n, cur_pos)):
            not_in_range[n] = abs(d - nanobots[n])

    # which one of these missed the best pos by the least distance
    nearest_miss = min(not_in_range, key=lambda x: not_in_range[x])
    miss_distance = not_in_range[nearest_miss]
    # print(f'nearest miss: {nearest_miss} with distance {miss_distance}')

    # move in every dimension the missed distance and calc the then in range nanobots
    new_in_ranges = dict()
    for dim in [(0, 0, miss_distance), (0, miss_distance, 0), (miss_distance, 0, 0)]:
        t = tuple(vector_add(cur_pos, dim))
        new_in_ranges[t] = len([1 for o in nanobots if manhattan_distance(o, t) <= nanobots[o]])

    # if moving resulted in more nanobots in range, set the new best pos
    for new_pos, new_in_range in new_in_ranges.items():
        if new_pos not in seen and new_in_range > cur_in_range:
            print(f'chosen dim:   {tuple(vector(new_pos, cur_pos))}')
            q.append((new_pos, new_in_range))
            in_range_positions[new_in_range].add(new_pos)
            print(f'new best pos: {new_pos} to {new_in_range} and distance to origin {manhattan_distance(cur_pos, (0, 0, 0))}')


max_in_range = max(in_range_positions)
print(max_in_range)
best_pos = min(in_range_positions[max_in_range], key=lambda p: manhattan_distance(p, (0, 0, 0)))
print(best_pos)

while True:
    dim = None
    for testdim in [(-1,-1,-1), (-1,-1,0), (-1,0,-1), (0,-1,-1), (0, 0, -1), (0, -1, 0), (-1, 0, 0)]:
        if len([1 for o in nanobots if manhattan_distance(o, vector_add(best_pos, testdim)) <= nanobots[o]]) >= max_in_range:
            # dim = testdim.index(-1)
            best_pos = vector_add(best_pos, testdim)
            dim = testdim
            break

    if dim is None:
        break

    while len([1 for o in nanobots if manhattan_distance(o, vector_add(best_pos, dim)) <= nanobots[o]]) >= max_in_range:
        best_pos = vector_add(best_pos, dim)
        dim = scalprod(dim, 2)

    print(best_pos)



# print(in_range_positions[max_in_range])
print(manhattan_distance(best_pos, (0, 0, 0)))
print('33537208 too low')
print('32119629 too low')
print('30947521 too low')
print('48202240')
print(datetime.datetime.now() - begin_time)
