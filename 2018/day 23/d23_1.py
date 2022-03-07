import datetime
import re

from aopython import manhattan_distance

begin_time = datetime.datetime.now()

nanobots = dict()
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        x, y, z, range = list(map(int, re.findall(r'-?\d+', line)))
        nanobots[(x, y, z)] = range

max_range_bot = max(nanobots, key=lambda b: nanobots[b])
max_range = nanobots[max_range_bot]
print(len([1 for b in nanobots if manhattan_distance(b, max_range_bot) <= max_range]))
print(datetime.datetime.now() - begin_time)
