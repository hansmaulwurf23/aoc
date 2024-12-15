import datetime

from aopython import vector_add

begin_time = datetime.datetime.now()

# this time in (y, x)!!
WALL, BOX, FREE = '#', 'O', '.'
UP, DOWN, LEFT, RIGHT = '^', 'v', '<', '>'
INVERSE = {RIGHT: LEFT, LEFT: RIGHT, UP: DOWN, DOWN: UP}
DIRS = {
    RIGHT: (0, 1),
    LEFT: (0, -1),
    UP: (-1, 0),
    DOWN: (1, 0),
}


def in_grid(y, x):
    global DIMX, DIMY
    return 0 <= x < DIMX and 0 <= y < DIMY


def value(y, x):
    global grid
    return grid[y][x] if in_grid(y, x) else '#'


def swap(oy, ox, ny, nx):
    global grid
    grid[oy][ox], grid[ny][nx] = grid[ny][nx], grid[oy][ox]


def move(cur, m):
    global grid
    d, inv = DIRS[m], DIRS[INVERSE[m]]

    front = tuple(vector_add(cur, d))
    while value(*front) == BOX:
        front = tuple(vector_add(front, d))

    # cannot move
    if value(*front) != FREE:
        return cur

    while front != cur:
        swap(*front, *(front := tuple(vector_add(front, inv))))

    return tuple(vector_add(cur, d))


def gps():
    global grid
    return sum(x + (100 * y) for y, l in enumerate(grid) for x, c in enumerate(l) if grid[y][x] == BOX)


grid, moves = [], []
with open('./input.txt') as f:
    lines = f.read().splitlines()
    for y, line in enumerate(lines):
        if not line:
            break
        grid.append(list(line))
        if (x := line.find('@')) >= 0:
            cur = (y, x)

    DIMX, DIMY = len(grid[0]), len(grid)
    moves = ''.join(lines[y + 1:])

for m in moves:
    cur = move(cur, m)

print(gps())
print(datetime.datetime.now() - begin_time)
