import datetime
import re

begin_time = datetime.datetime.now()

blocked = []
MAXIP = 4294967295

with open('./input.txt') as f:
    while line := f.readline().rstrip():
        # nice to forget the -? and for once it all makes sense :)
        blocked.append(tuple(map(int, re.findall(r'\d+', line))))

blocked = list(sorted(blocked))

x = 0
for l, h in blocked:
    if l > x:
        break
    elif x < h:
        x = h + 1

print(f'part 1 {x}')

x = 0
c = 0
maxh = 0
for l, h in blocked:
    maxh = max(maxh, h)
    if l > x:
        c += l-x
        x = h + 1
    elif x < h:
        x = h + 1

if maxh < MAXIP:
    c += MAXIP - maxh
print(f'part 2 {c}')
print(datetime.datetime.now() - begin_time)
