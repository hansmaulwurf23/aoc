import datetime
from collections import Counter
begin_time = datetime.datetime.now()

counters = dict()
with open('./input.txt') as f:
    data = f.readlines()[0].rstrip()

l_min_zeros = None
for l in range(len(data) // (25 * 6)):
    counters[l] = Counter(data[(l * 25 * 6):((l + 1) * 25 * 6)])
    if l_min_zeros is None or counters[l_min_zeros]['0'] > counters[l]['0']:
        l_min_zeros = l

print(counters[l_min_zeros]['1'] * counters[l_min_zeros]['2'])
print(datetime.datetime.now() - begin_time)
