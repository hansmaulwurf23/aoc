import datetime
from functools import reduce
from itertools import combinations
from collections import defaultdict
from aopython import manhattan_distance

begin_time = datetime.datetime.now()

points = []
distances = defaultdict(dict)
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        points.append(tuple(map(int, line.split(','))))

print(f'read {len(points)} points')
for a, b in combinations(sorted(points), 2):
    distances[a][b] = manhattan_distance(a, b)
    distances[b][a] = distances[a][b]

print(f'calculated {len(distances)} ({sum([len(s) for s in distances.values()])}) distances')
constellations = set()
for p, others in distances.items():
    cur_const = {p} | {o for o in others.keys() if others[o] <= 3}
    constellations.add(frozenset(cur_const))


while True:
    # print(f'{len(reduce(lambda a, b: a | b, constellations))} distinct stars in {len(constellations)} constellations')
    merged = False
    for a, b in combinations(constellations, 2):
        if a & b:
            if a < b:
                constellations.remove(a)
            elif b < a:
                constellations.remove(b)
            else:
                constellations.add(frozenset(a | b))
                constellations.remove(a)
                constellations.remove(b)
            merged = True
            break
    if not merged:
        break

print(len(constellations))
print(datetime.datetime.now() - begin_time)
