import re
import datetime
from collections import defaultdict

begin_time = datetime.datetime.now()

entries = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        entries.append(line)

entries = list(sorted(entries))
i = 0
sleep_histo = defaultdict(lambda: defaultdict(lambda: 0))
sleep_sum = defaultdict(lambda: 0)
while i < len(entries):
    if match := re.match('.*(\d\d:\d\d).*Guard.*#(\d+) begins.*', entries[i]):
        shift, guard = match.groups()
        i += 1
    elif match := re.match(r'.*(\d\d:\d\d).*falls.*(\d\d:\d\d).*wakes.*', ''.join(entries[i:i + 2])):
        sleep, wake = list(map(lambda g: int(g.split(':')[1]), match.groups()))
        sleep_sum[guard] += (wake - sleep)
        for m in range(sleep, wake):
            sleep_histo[guard][m] += 1
        i += 2
    else:
        print('wtf')

sleepy_guard = max(sleep_sum, key=sleep_sum.get)
histo = sleep_histo[sleepy_guard]
best_minute = max(histo, key=histo.get)
print(sleepy_guard, best_minute)
print(int(sleepy_guard) * best_minute)
print(datetime.datetime.now() - begin_time)
