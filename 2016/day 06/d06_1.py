import datetime
from collections import Counter, defaultdict

begin_time = datetime.datetime.now()

idx_counters = defaultdict(lambda: Counter())
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        for idx, c in enumerate(line):
            idx_counters[idx].update(c)

print(''.join([c.most_common(1)[0][0] for i, c in idx_counters.items()]))
print(datetime.datetime.now() - begin_time)
