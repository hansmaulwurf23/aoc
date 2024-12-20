import datetime
from collections import deque, defaultdict

from aopython import vector_add, manhattan_distance, vector_mul

begin_time = datetime.datetime.now()

NORTH, EAST, SOUTH, WEST = range(4)
DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
FREE, WALL = '.', '#'


def in_grid(x, y):
    return 0 <= x < DIMX and 0 <= y < DIMY


def mapv(x, y):
    return grid[y][x] if in_grid(x, y) else WALL


def write_path(steps, path):
    with open(f'/tmp/aoc/d20/{steps}.txt', 'w') as f:
        for y, line in enumerate(grid):
            for x, c in enumerate(line):
                if (x, y) in path:
                    f.write('O')
                else:
                    f.write(c)
            f.write('\n')


def bfs(start, end):
    q = deque()
    q.append((start, 0))
    seen = set([start])
    times = {start: 0}

    while q:
        cur, steps = q.popleft()

        if cur == end:
            return times

        for nxt in [tuple(vector_add(cur, d)) for d in DIRS]:
            if nxt not in seen and mapv(*nxt) == FREE:
                q.append((nxt, steps + 1))
                seen.add(nxt)
                times[nxt] = steps + 1


def find_valid_cheats(times):
    cheats = dict()
    for pos in times:
        for nxt in [n for n in [tuple(vector_add(pos, vector_mul(d, 2))) for d in DIRS] if n in times and times[n] < times[pos]]:
            time_saved = times[pos] - times[nxt] - 2
            if time_saved > 0:
                cheats[(pos, nxt)] = time_saved
    return cheats


def find_vicinity_cheats(times, md):
    cheats = dict()
    for pos in times:
        for x, y in [(x, y) for x in range(-md, md+1, 1) for y in range(-md, md+1, 1) if abs(x) + abs(y) <= md]:
            nxt = tuple(vector_add(pos, (x, y)))
            if nxt in times and times[pos] > times[nxt]:
                time_saved = times[pos] - times[nxt] - abs(x) - abs(y)
                if time_saved > 0:
                    cheats[(tuple(reversed(pos)), tuple(reversed(nxt)))] = time_saved
    return cheats

grid = []
with open('./input.txt') as f:
    y = 0
    while line := f.readline().rstrip():
        grid.append([])
        for x, c in enumerate(line):
            if c == 'E':
                end = (x, y)
                grid[y].append(FREE)
            elif c == 'S':
                start = (x, y)
                grid[y].append(FREE)
            else:
                grid[y].append(c)
        y += 1
    DIMX, DIMY = len(grid[0]), len(grid)

times = bfs(start, end)
# cheats = find_valid_cheats(times)
cheats = find_vicinity_cheats(times, 2)
print(f'part 1: {sum(c >= 100 for c in cheats.values())}')
cheats = find_vicinity_cheats(times, 20)
print(f'part 2: {sum(c >= 100 for c in cheats.values())}')
print('986081 too low')
print(datetime.datetime.now() - begin_time)
