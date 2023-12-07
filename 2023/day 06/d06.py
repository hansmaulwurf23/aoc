import datetime
import math
from functools import reduce
from aopython import abc_formula

begin_time = datetime.datetime.now()


def calc_dist(t, max_t):
    return (max_t - t) * t


def count_possible_ways(time, distance):
    sols = abc_formula(-1, time, -distance)
    s1, s2 = math.floor(sols[0]), math.ceil(sols[1])
    if calc_dist(s1, time) <= distance:
        s1 += 1
    if calc_dist(s2, time) <= distance:
        s2 -= 1
    return s2 - s1 + 1


with open('./input.txt') as f:
    lines = list(map(lambda l: l.split(':')[-1], f.readlines()))

times = map(int, lines[0].split())
dists = map(int, lines[1].split())
print(f'part 1: {reduce(lambda x, y: x * y, [count_possible_ways(t, d) for t, d in zip(times, dists)])}')

time = int(lines[0].strip().replace(' ', ''))
distance = int(lines[1].strip().replace(' ', ''))
print(f'part 2: {count_possible_ways(time, distance)}')
print(datetime.datetime.now() - begin_time)
