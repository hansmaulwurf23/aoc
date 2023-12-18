import datetime
from heapq import heappush, heappop
from aopython import vector_add

begin_time = datetime.datetime.now()

NORTH, SOUTH, EAST, WEST = range(4)
ALL_DIRS = range(4)
DIRS = [(0, -1), (0, 1), (+1, 0), (-1, 0)]
OPPO = [SOUTH, NORTH, WEST, EAST]

def get_loss(pos):
    global grid
    x, y = pos
    return grid[y][x]

def in_grid(pos):
    global grid
    x, y = pos
    return 0 <= y < len(grid) and 0 <= x < len(grid[y])

def flow(start, end, max_repeat, min_repeat):
    global grid
    seen = set()
    q = [(0, start, None, 0)]

    while q:
        loss, pos, dir, repeat = heappop(q)

        if pos == end and repeat >= min_repeat:
            return loss

        if (pos, dir, repeat) in seen:
            continue
        seen.add((pos, dir, repeat))

        if repeat >= min_repeat or dir is None:
            for ndir in ALL_DIRS:
                if (dir is None or ndir != OPPO[dir]) and ndir != dir:
                    npos = vector_add(pos, DIRS[ndir])
                    if in_grid(npos):
                        heappush(q, (loss + get_loss(npos), tuple(npos), ndir, 1))

        # keep on flowing in a freeee woooooorld
        if repeat < max_repeat and dir is not None:
            npos = vector_add(pos, DIRS[dir])
            if in_grid(npos):
                heappush(q, (loss + get_loss(npos), tuple(npos), dir, repeat + 1))

with open('./input.txt') as f:
    grid = [list(map(int, list(l))) for l in f.read().splitlines()]

start = (0, 0)
end = (len(grid[0]) - 1, len(grid) - 1)

p1 = flow(start, end, 3, 1)
print(f'part 1: {p1}')
assert p1 in [758, 102]

p2 = flow(start, end, 10, 4)
print(f'part 2: {p2}')
assert p2 in [892, 94]
print(datetime.datetime.now() - begin_time)
