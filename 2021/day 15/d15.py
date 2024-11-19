import datetime
from heapq import heappush, heappop
from aopython import vector_add

begin_time = datetime.datetime.now()
DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def in_grid(x, y, repeat):
    return 0 <= x < DIMX * repeat and 0 <= y < DIMY * repeat


def grid_val(x, y, repeat):
    global grid
    v = grid[y % DIMY][x % DIMX] + (x // DIMX) + (y // DIMY)
    v = v if v < 10 else v - 9
    return v

def walk(start, end, repeat=1):
    global grid

    q = []
    seen = set()
    heappush(q, (0, start))

    while q:
        cost, node = heappop(q)

        if node == end:
            return cost

        if node in seen:
            continue
        seen.add(node)

        for nx, ny in [n for n in map(lambda d: vector_add(node, d), DIRS) if in_grid(*n, repeat)]:
            heappush(q, (cost + grid_val(nx, ny, repeat), tuple((nx, ny))))


grid = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        grid.append(list(map(int, line)))

DIMX, DIMY = len(grid[0]), len(grid)
start, end = (0, 0), (DIMX - 1, DIMY - 1)
print(f'part 1: {walk(start, end)}')
start, end = (0, 0), (DIMX*5 - 1, DIMY*5 - 1)
print(f'part 2: {walk(start, end, repeat=5)}')

print(datetime.datetime.now() - begin_time)
