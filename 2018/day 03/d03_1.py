import datetime
from collections import defaultdict

begin_time = datetime.datetime.now()
canvas = defaultdict(set)


def process_claim(line):
    id, rest = line.split(' @ ')
    id = id.replace('#', '')
    origin, rest = rest.split(': ')
    origin = list(map(int, origin.split(',')))
    size = list(map(int, rest.split('x')))

    for x in range(origin[0], origin[0] + size[0]):
        for y in range(origin[1], origin[1] + size[1]):
            canvas[x, y].add(id)


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        process_claim(line)

overlapping = sum(map(lambda x: len(x) > 1, canvas.values()))
print(overlapping)
print(datetime.datetime.now() - begin_time)