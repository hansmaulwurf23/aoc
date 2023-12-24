import datetime
from collections import deque
from aopython import vector_add

begin_time = datetime.datetime.now()

SLOP = ('v', '^', '>', '<')
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
    graph = {start:dict()}
    q = deque([(start, start, 0)])
    seen = {start}

    while q:
        pos, last_node, steps = q.popleft()
        x, y = pos

        if pos == end:
            graph[last_node][end] = steps

        force_dir = None if grid[y][x] not in SLOP else DIRS[SLOP.index(grid[y][x])]
        adjacents = [(a, d) for (a, d) in [(tuple(vector_add(pos, d)), d) for d in DIRS if force_dir is None or force_dir == d] if in_grid(*a)]
        # neighbours ignore slopes
        neighbours = [(n, d) for (n, d) in adjacents if _grid(*n) != '#']
        adjacents = [a for (a, d) in neighbours if _grid(*a) == '.' or DIRS[SLOP.index(_grid(*a))] == d]

        # store crossing as nodes
        if len(neighbours) > 2:
            graph[last_node][pos] = steps
            if pos not in graph:
                graph[pos] = dict()
            last_node = pos
            steps = 0

        # go in every direction
        for a in adjacents:
            if a in seen:
                # if seen but on a crossing store distance and stop
                if a in graph and a != start and a != last_node:
                    graph[last_node][a] = steps + 1
            else:
                q.append((a, last_node, steps+1))
                seen.add(a)

    return dict(graph)

def walk(pos, end):
    global graph
    if pos == end:
        return 0

    return max([steps + walk(npos, end) for npos, steps in graph[pos].items()])


with open('./input.txt') as f:
    grid = [list(l) for l in f.read().splitlines()]

start = (grid[0].index('.'), 0)
end =   (grid[-1].index('.'), len(grid) - 1)
graph = build_graph(start, end)
# print_grid()
p1 = walk(start, end)
print(f'part 1: {p1}')
assert p1 in [2326, 94]

print(datetime.datetime.now() - begin_time)
