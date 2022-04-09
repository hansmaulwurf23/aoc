import datetime
from itertools import count

begin_time = datetime.datetime.now()
layers = []


def run(layers, delay):
    for depth, range in layers:
        time = depth + delay
        scanner = time % (2 * (range - 1))
        if scanner == 0:
            return True

    return False


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        depth, range = list(map(int, line.split(': ')))
        layers.append([depth, range])


for d in count(1):
    caught = run(layers, d)
    if not caught:
        print(d)
        break

print(datetime.datetime.now() - begin_time)
