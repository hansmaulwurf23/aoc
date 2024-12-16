import datetime
from heapq import heappush, heappop

from aopython import vector_add

begin_time = datetime.datetime.now()

NORTH, EAST, SOUTH, WEST = range(4)
DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
WALL, FREE = '#', '.'
COST_MOVE, COST_TURN = 1, 1000


def in_grid(x, y):
    return 0 <= x < DIMX and 0 <= y < DIMY


def mapv(x, y):
    return map[y][x] if in_grid(x, y) else WALL


def walk(start, end):
    q, seen = [], set()
    heappush(q, (0, start, EAST, {start}))
    best_cost, best_path = None, None

    while q:
        cost, pos, dir, path = heappop(q)
        seen.add((pos, dir))

        if best_cost is not None and cost > best_cost:
            continue

        if pos == end:
            if best_cost is None:
                best_cost = cost
                best_path = path
            elif cost == best_cost:
                best_path |= path

        # MOVE
        nxt = tuple(vector_add(pos, DIRS[dir]))
        if mapv(*nxt) == FREE and (nxt, dir) not in seen:
            heappush(q, [cost + COST_MOVE, nxt, dir, path | {nxt}])

        # TURN
        for ndir in [(dir + n) % 4 for n in [-1, 1]]:
            if (pos, ndir) not in seen:
                heappush(q, [cost + COST_TURN, pos, ndir, path])

    return best_cost, len(best_path)


map = [[]]
with open('./input.txt') as f:
    y = 0
    while line := f.readline().rstrip():
        for x, c in enumerate(line):
            if c == 'E':
                end = (x, y)
                map[y].append(FREE)
            elif c == 'S':
                start = (x, y)
                map[y].append(FREE)
            else:
                map[y].append(c)
        y += 1
        map.append([])
    DIMX, DIMY = len(map[0]), len(map)

p1, p2 = walk(start, end)
print(f'part 1: {p1}')
print(f'part 2: {p2}')
assert p1 in (99460, 11048, 7036)
assert p2 in (500, 64, 45)
print(datetime.datetime.now() - begin_time)
