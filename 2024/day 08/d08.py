import datetime
from collections import defaultdict
from itertools import permutations
from aopython import vector, vector_add

begin_time = datetime.datetime.now()

def in_grid(x, y):
    global DIMX, DIMY
    return 0 <= x < DIMX and 0 <= y < DIMY


antennas = defaultdict(list)
with open('./input.txt') as f:
    lines = list(map(lambda l: l.rstrip(), f.readlines()))
    DIMX, DIMY = len(lines[0]), len(lines)
    for x, y, c in [(x, y, c) for y, l in enumerate(lines) for x, c in enumerate(l) if c != '.']:
        antennas[c].append((x, y))

antinodes = set()
for _, fants in antennas.items():
    for a, b in permutations(fants, 2):
        v = vector(a, b)
        ant = tuple(vector_add(v, b))
        if in_grid(*ant):
            antinodes.add(ant)

print(f'part 1: {len(antinodes)}')

antinodes = set()
for _, fants in antennas.items():
    for a, b in permutations(fants, 2):
        v, ant = vector(a, b), tuple(a)
        while in_grid(*ant):
            antinodes.add(ant)
            ant = tuple(vector_add(v, ant))

print(f'part 2: {len(antinodes)}')
print(datetime.datetime.now() - begin_time)
