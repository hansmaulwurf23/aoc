import datetime

from aopython import vector_add, manhattan_distance

begin_time = datetime.datetime.now()

# this time in (y, x)!!
WALL, LBOX, RBOX, FREE = '#', '[', ']', '.'
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


def lrmove(cur, m):
    global grid
    d, inv = DIRS[m], DIRS[INVERSE[m]]

    front = tuple(vector_add(cur, d))
    while value(*front) in (LBOX, RBOX):
        front = tuple(vector_add(front, d))

    # cannot move
    if value(*front) != FREE:
        return cur

    while front != cur:
        swap(*front, *(front := tuple(vector_add(front, inv))))

    return tuple(vector_add(cur, d))


def udmove(cur, m):
    global grid
    d, inv = DIRS[m], DIRS[INVERSE[m]]
    affected = {cur}
    to_inspect = {cur}

    while to_inspect:
        pos = to_inspect.pop()
        front = tuple(vector_add(pos, d))
        if value(*front) == WALL:
            return cur

        if value(*front) == FREE:
            continue

        if value(*front) == LBOX:
            new = {front, tuple(vector_add(front, DIRS[RIGHT]))}
        elif value(*front) == RBOX:
            new = {front, tuple(vector_add(front, DIRS[LEFT]))}
        else:
            raise RuntimeError('invalid element')

        to_inspect |= new
        affected |= new

    to_swap = sorted(affected) if m == UP else sorted(affected, reverse=True)
    for s in to_swap:
        swap(*s, *vector_add(s, d))

    return tuple(vector_add(cur, d))


def gps():
    global grid
    return sum(x + (100 * y) for y, l in enumerate(grid) for x, c in enumerate(l) if grid[y][x] == LBOX)


grid, moves = [[]], []
with open('./input.txt') as f:
    lines = f.read().splitlines()
    for y, line in enumerate(lines):
        if not line:
            break
        for x, c in enumerate(line):
            if c == '@':
                cur = (y, x * 2)
                grid[-1].extend('@.')
            elif c == 'O':
                grid[-1].extend('[]')
            else:
                grid[-1].extend(c * 2)
        grid.append([])

    DIMX, DIMY = len(grid[0]), len(grid)
    moves = ''.join(lines[y + 1:])

for m in moves:
    if m in (LEFT, RIGHT):
        cur = lrmove(cur, m)
    else:
        cur = udmove(cur, m)

print(gps())
print(datetime.datetime.now() - begin_time)
