import datetime
from collections import defaultdict, Counter
from functools import reduce

begin_time = datetime.datetime.now()

repeat_counts = defaultdict(lambda : 0)


def calc_repeats(input):
    return set([c for (l, c) in Counter(input).items() if 1 < c < 4])


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        r = calc_repeats(line)
        if r:
            for c in r:
                repeat_counts[c] += 1

print(repeat_counts)
print(reduce(lambda a, b: a * b, repeat_counts.values()))
print(datetime.datetime.now() - begin_time)
