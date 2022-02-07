import datetime
from itertools import combinations

begin_time = datetime.datetime.now()

boxids = []

with open('./input.txt') as f:
    while line := f.readline().rstrip():
        boxids.append(line)


for box_a, box_b in combinations(boxids, 2):
    oneshot = -1
    i = 0
    for a, b in zip(box_a, box_b):
        if a != b:
            if oneshot == -1:
                oneshot = i
            else:
                break

        i += 1

    if i == len(box_a):
        print(''.join([box_a[0:oneshot], box_a[oneshot+1:]]))
        break

print(datetime.datetime.now() - begin_time)
