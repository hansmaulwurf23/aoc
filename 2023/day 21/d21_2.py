import datetime
from collections import deque
import showgrid
from aopython import vector_add, min_max_2d

begin_time = datetime.datetime.now()

N, E, S, W = range(4)
DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))

def is_plot(pos):
    global grid
    x, y = pos
    return grid[y % SIZE][x % SIZE] != '#'

def in_grid(pos, no_repeat=False):
    global SIZE
    x, y = pos
    return not no_repeat or (0 <= y < SIZE and 0 <= x < SIZE)

def adjacents(pos, no_repeat=False):
    global grid
    return [tuple(pos) for pos in [tuple(vector_add(d, pos)) for d in DIRS] if is_plot(pos) and in_grid(pos, no_repeat)]

def print_grid(seen, walls, filename='plot.png'):
    global grid, SIZE
    fx, tx, fy, ty = min_max_2d(seen)
    w = set()
    for deltay in range(fx // SIZE, tx // SIZE + 1):
        for deltax in range(fy // SIZE, ty // SIZE + 1):
            for wx, wy in walls:
                w.add((deltax * SIZE + wx, deltay * SIZE + wy))
    plt = showgrid.show_grid(seen, highlights=w, s=1, highlightsize=1, fh=20, fw=20, no_show=True)
    plt.savefig(filename)
    print(fx, tx, fy, ty)

def bfs(start, max_steps, no_repeat=False):
    valids = set()
    seen = {start}
    q = deque([(max_steps, start)])

    while q:
        steps, pos = q.popleft()

        if steps % 2 == 0:
            valids.add(pos)

        for a in adjacents(pos, no_repeat):
            if a not in seen and steps:
                seen.add(a)
                q.append((steps - 1, a))

    return valids


with open('./input.txt') as f:
    grid = [list(line) for line in f.read().splitlines()]

# sample and real input is quadratic
SIZE = len(grid)
GRID_RADIUS = SIZE // 2
MAX_STEPS = 26501365
GRIDS = (MAX_STEPS - GRID_RADIUS) // SIZE
# print(SIZE, GRID_RADIUS, MAX_STEPS, GRIDS, MAX_STEPS - (GRIDS * SIZE))

walls = set()
for y, line in enumerate(grid):
    for x, c in enumerate(line):
        if c == 'S':
            start = (x, y)
        # elif c == '#':
        #     walls.add((x, y))

walls |= set([(x, y) for y in [0, SIZE-1] for x in range(0, SIZE)])
walls |= set([(x, y) for x in [0, SIZE-1] for y in range(0, SIZE)])

# some plots to get an idea
# valids = bfs(start, SIZE)
# print_grid(valids, walls, f'plot_00_1_SIZE.png')
# for repeats in [0, 1, 2, 3, 4]:
#     valids = bfs(start, GRID_RADIUS + (repeats * SIZE))
#     print_grid(valids, walls, f'plot_65_{repeats}_SIZE.png')
# for repeats in [1, 2, 3]:
#     valids = bfs(start, repeats * SIZE)
#     print_grid(valids, walls, f'plot_00_{repeats}_SIZE.png')

T = bfs(start, GRID_RADIUS + (2*SIZE))
sizes = [[0 for _ in range(5)] for _ in range(5)]
for px, py in T:
    gx, gy = (2*SIZE + px) // SIZE, (2*SIZE + py) // SIZE
    sizes[gy][gx] += 1

def calc_tot(sizes, repeats):
    tot = 0
    # edges
    tot += sizes[0][2] + sizes[-1][2] + sizes[2][0] + sizes[2][-1]
    # internals red
    tot += ((repeats - 1) ** 2 * sizes[2][2])
    # internals blue
    tot += (repeats ** 2 * sizes[2][3])
    # edges off
    tot += (repeats - 1) * (sizes[1][1] + sizes[1][-2] + sizes[-2][1] + sizes[-2][-2])
    # small corners
    tot += repeats * (sizes[1][0] + sizes[1][-1] + sizes[-2][0] + sizes[-2][-1])
    return tot

print(calc_tot(sizes, GRIDS))
print(datetime.datetime.now() - begin_time)
