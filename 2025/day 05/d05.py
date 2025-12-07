import datetime

begin_time = datetime.datetime.now()

valids = []
fresh = 0
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        strt, end = list(map(int, line.split('-')))
        valids.append((strt, end))

    while line := f.readline().rstrip():
        id = int(line)
        if any((strt, end) for (strt, end) in valids if strt <= id <= end):
            fresh += 1

valids.sort()
merged = []
for strt, end in valids:
    if not merged:
        merged.append((strt, end))
    elif merged[-1][1] < strt:
        merged.append((strt, end))
    elif merged[-1][1] < end:
        merged[-1] = (merged[-1][0], end)

print(f'part 1: {fresh}')
print(f'part 2: {sum(end - strt + 1 for strt, end in merged)}')
assert fresh in (509, 3)
print(datetime.datetime.now() - begin_time)
