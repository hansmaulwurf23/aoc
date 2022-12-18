import datetime
from collections import deque

from aopython import vector_add

begin_time = datetime.datetime.now()
ADJACENTS = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]


def adjacents(p):
    for d in ADJACENTS:
        yield tuple(vector_add(p, d))


lava = set()
air = set()
clusters = []
sides = 0


def get_cluster(root):
    q = deque()
    q.append(root)
    seen = {root}
    surface = 0
    while q:
        cur_pos = q.popleft()

        if cur_pos[0] not in range_x or cur_pos[1] not in range_y or cur_pos[2] not in range_z:
            return True, 0, seen

        for a in adjacents(cur_pos):
            if a in lava:
                surface += 1
            else:
                if a not in seen:
                    q.append(a)
                    seen.add(a)

    return False, surface, seen


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        lava.add(tuple(map(int, line.split(','))))

range_x = range(min(map(lambda e: e[0], lava)), max(map(lambda e: e[0], lava)))
range_y = range(min(map(lambda e: e[1], lava)), max(map(lambda e: e[1], lava)))
range_z = range(min(map(lambda e: e[2], lava)), max(map(lambda e: e[2], lava)))
print(range_x, range_y, range_z)

for p in lava:
    for a in adjacents(p):
        if a not in lava:
            air.add(a)
            sides += 1

inspect = set(air)
while inspect:
    pos = inspect.pop()
    open_cluster, surface, positions = get_cluster(pos)
    if not open_cluster:
        sides -= surface
        # print(f'closed cluster with surface {surface} and pos {positions} -> {sides}')
        # remove all positions in this cluster from set of to inspect air cubes
        inspect -= positions

print(sides)
print(datetime.datetime.now() - begin_time)
