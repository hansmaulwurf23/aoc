import datetime
begin_time = datetime.datetime.now()

MALUS = {')': 3, ']': 57, '}': 1197, '>': 25137}
COST = {')': 1, ']': 2, '}': 3, '>': 4}
INV = {')': '(', '}': '{', ']': '[', '>': '<'}
for k in list(INV.keys()):
    INV[INV[k]] = k

def is_valid(s: str) -> bool:
    chunk = []
    for c in s:
        if c in ('(', '{', '[', '<'):
            chunk.append(c)
        elif c in INV:
            if chunk and chunk[-1] == INV[c]:
                chunk.pop()
            else:
                return MALUS[c]

    cost = 0
    for c in reversed(chunk):
        cost = cost * 5 + COST[INV[c]]
    return -cost


mp, costs = 0, []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        m = is_valid(line)
        mp += max(0, m)
        if m < 0:
            costs.append(-m)


print(f'part 1: {mp}')
print(f'part 2: {sorted(costs)[len(costs) // 2]}')
print(datetime.datetime.now() - begin_time)
