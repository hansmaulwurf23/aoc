import datetime
import re
from collections import defaultdict
from itertools import combinations

from particle import Particle

begin_time = datetime.datetime.now()
particles = dict()

with open('./input.txt') as f:
    idx = 0
    while line := f.readline().rstrip():
        particles[idx] = Particle(idx, list(map(int, re.findall(r'-?\d+', line))))
        idx += 1

assert particles[93].collides(particles[94]) == 14
assert particles[37].collides(particles[38]) == 12
assert particles[115].collides(particles[116]) == 10

colls = defaultdict(set)
for p1, p2 in combinations(particles.values(), 2):
    if (t := p1.collides(p2)) > 0:
        colls[t] |= {(p1, p2)}

for k in sorted(colls.keys()):
    rm = []
    for a, b in colls[k]:
        if a.id in particles and b.id in particles:
            rm.append(a.id)
            rm.append(b.id)
    rm = sorted(list(set(rm)))
    # print(f'removing {rm} time: {k}')
    for r in rm:
        particles.pop(r)

print(len(particles))
print(datetime.datetime.now() - begin_time)
