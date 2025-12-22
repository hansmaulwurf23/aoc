import datetime
from functools import reduce
from itertools import combinations
begin_time = datetime.datetime.now()

# MAX_SHORTEST_CONNECTIONS, FILENAME = (10, 'code00.txt')
MAX_SHORTEST_CONNECTIONS, FILENAME = (1000, 'input.txt')


def euclid_distance(a, b):
    return sum([(s - t)**2 for s, t in zip(a, b)])


boxes = []
with open(FILENAME) as f:
    while line := f.readline().rstrip():
        boxes.append(tuple(map(int, line.split(','))))

dists = []
for a, b in combinations(boxes, 2):
    dists.append((euclid_distance(a, b), a, b))

circuits = 0
dists.sort()
cluster = []
for d, a, b in dists[:MAX_SHORTEST_CONNECTIONS]:
    ca = [e for e in cluster if e & {a}]
    cb = [e for e in cluster if e & {b}]
    # print(d, a, b, ca)
    if not ca and not cb:
        cluster.append({a, b})
        circuits += 1
    elif not cb:
        ca[0] |= {b}
        circuits += 1
    elif not ca:
        cb[0] |= {a}
        circuits += 1
    elif ca == cb:
        pass
    else:
        ca[0] |= cb[0]
        cluster.remove(cb[0])

part1 = reduce(lambda x, y: x*y, sorted([len(e) for e in cluster], reverse=True)[:3])
print(f'Part 1: {part1}')
assert part1 in (133574, 40)

for d, a, b in dists[MAX_SHORTEST_CONNECTIONS:]:
    ca = [e for e in cluster if e & {a}]
    cb = [e for e in cluster if e & {b}]
    # print(d, a, b, ca)
    if not ca and not cb:
        cluster.append({a, b})
        circuits += 1
    elif not cb:
        ca[0] |= {b}
        circuits += 1
    elif not ca:
        cb[0] |= {a}
        circuits += 1
    elif ca == cb:
        pass
    else:
        ca[0] |= cb[0]
        cluster.remove(cb[0])

    if len(cluster) == 1 and len(cluster[0]) == len(boxes):
        break

part2 = a[0] * b[0]
print(f'Part 2: {part2}')
assert part2 in (2435100380, 25272)
print(datetime.datetime.now() - begin_time)
