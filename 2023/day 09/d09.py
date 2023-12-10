import datetime
from collections import deque
from itertools import pairwise

begin_time = datetime.datetime.now()

def extrapolate(sequence):
    diffs, vals = [], sequence
    while not all([d == 0 for d in vals]):
        diffs.append(deque([b-a for a, b in pairwise(vals)]))
        vals = list(diffs[-1])

    diffs[-1].append(0)
    diffs[-1].appendleft(0)
    for di in range(len(diffs) - 2, -1, -1):
        diffs[di].append(diffs[di][-1] + diffs[di+1][-1])
        diffs[di].appendleft(diffs[di][0] - diffs[di+1][0])

    sequence.append(sequence[-1] + diffs[0][-1])
    sequence.appendleft(sequence[0] - diffs[0][0])


with open('./input.txt') as f:
    sequences = [deque(map(int, l.split())) for l in f.read().splitlines()]

for seq in sequences:
    extrapolate(seq)

part1 = sum(map(lambda l: l[-1], sequences))
assert part1 in [114, 1969958987]
print(f'part 1: {part1}')

part2 = sum(map(lambda l: l[0], sequences))
assert part2 in [2, 1068]
print(f'part 2: {part2}')

print(datetime.datetime.now() - begin_time)
