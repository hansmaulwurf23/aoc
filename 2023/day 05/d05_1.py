import datetime
import math
import re

begin_time = datetime.datetime.now()

mappings = [dict()]
with open('./input.txt') as f:
    lines = list(map(lambda x: x.rstrip(), f.readlines()))
    seeds = list(map(int, re.findall(f'\d+', lines[0])))
    i = 3
    while i < len(lines):
        if not lines[i].rstrip():
            i += 2
            mappings.append(dict())
        else:
            dest, source, size = map(int, lines[i].split())
            mappings[-1][range(source, source + size)] = dest - source
            i += 1

min_loc = math.inf
for seed in seeds:
    for mapping in mappings:
        for sr, delta in mapping.items():
            if seed in sr:
                seed += delta
                break
    min_loc = min(min_loc, seed)

print(min_loc)
print(datetime.datetime.now() - begin_time)
