import datetime
from collections import defaultdict
begin_time = datetime.datetime.now()

orbits = defaultdict(list)
with open('./input.txt') as f:
    while line  := f.readline().rstrip():
        center, orbiter = line.split(')')
        orbits[center].append(orbiter)


def sum_orbits(orbits, start, orbit_distance):
    res = len(orbits[start]) * orbit_distance
    for trabant in orbits[start]:
        res += sum_orbits(orbits, trabant, orbit_distance + 1)

    return res

print(sum_orbits(orbits, 'COM', 1))
print(datetime.datetime.now() - begin_time)
