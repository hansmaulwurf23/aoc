import datetime
import re
from collections import defaultdict
from particle import Particle

begin_time = datetime.datetime.now()

particle_by_acc = defaultdict(list)
with open('./input.txt') as f:
    idx = 0
    while line := f.readline().rstrip():
        p = Particle(idx, list(map(int, re.findall(r'-?\d+', line))))
        particle_by_acc[p.absolute_acceleration()].append(p)
        idx += 1


min_acc = min(particle_by_acc.keys())
min_dst = min(map(lambda p: p.center_distance(), particle_by_acc[min_acc]))
print(list(filter(lambda p: p.center_distance() == min_dst, particle_by_acc[min_acc]))[0].id)
print(datetime.datetime.now() - begin_time)
