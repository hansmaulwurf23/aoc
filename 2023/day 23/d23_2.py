import datetime
import math
from collections import defaultdict
from aopython import vector_add

begin_time = datetime.datetime.now()

DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def print_grid():
    global grid, graph
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if (x, y) in graph:
                print('X', end='')
            else:
                print(c, end='')
        print('')

def in_grid(x, y):
    global grid
    return 0 <= y < len(grid) and 0 <= x < len(grid[y])

def _grid(x, y):
    return grid[y][x]

def build_graph(start, end):
    global grid
    crossings = [start, end]
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c != '#' and len([a for a in [tuple(vector_add((x, y), d)) for d in DIRS] if in_grid(*a) and _grid(*a) != '#']) > 2:
                crossings.append((x, y))

    graph = defaultdict(dict)
    for c in crossings:
        lifo = [(0, c)]
        seen = {(c)}

        while lifo:
            steps, pos = lifo.pop()

            if steps != 0 and pos in crossings:
                graph[c][pos] = steps
                continue

            for a in [a for a in [tuple(vector_add(pos, d)) for d in DIRS] if in_grid(*a) and _grid(*a) != '#']:
                if a not in seen:
                    lifo.append((steps + 1, a))
                    seen.add(a)

    return graph

def walk(pos, end):
    global graph, walk_seen
    if pos == end:
        return 0

    walk_seen.add(pos)
    r = max([steps + walk(npos, end) for npos, steps in graph[pos].items() if npos not in walk_seen] + [-math.inf])
    walk_seen.remove(pos)
    return r

with open('./input.txt') as f:
    grid = [list(l) for l in f.read().splitlines()]

start = (grid[0].index('.'), 0)
end =   (grid[-1].index('.'), len(grid) - 1)
graph = build_graph(start, end)
walk_seen = set()

p2 = walk(start, end)
print(f'part 2: {p2}')
assert p2 in [6574, 154]
print(datetime.datetime.now() - begin_time)
