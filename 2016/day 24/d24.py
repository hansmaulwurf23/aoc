import datetime
from collections import deque, defaultdict
from itertools import combinations

from aopython import vector_add

begin_time = datetime.datetime.now()

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def read_items(grid):
    items = dict()
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c.isdigit():
                items[c] = (x, y)
    return items


def adjacents(pos, grid):
    for newpos in [vector_add(pos, d) for d in DIRS]:
        nx, ny = newpos
        if 0 <= newpos[0] < len(grid[0]) and 0 <= newpos[1] < len(grid) and grid[newpos[1]][newpos[0]] != '#':
            yield tuple(newpos)


def bfs(start, end, grid, nodes):
    q = deque([(start, 0)])
    seen = set()
    additionals = dict()

    while q:
        cur_pos, steps = q.popleft()

        if cur_pos == end:
            return steps, additionals

        if grid[cur_pos[1]][cur_pos[0]] in nodes:
            additionals[grid[cur_pos[1]][cur_pos[0]]] = steps

        for a in adjacents(cur_pos, grid):
            if a not in seen:
                q.append((a, steps + 1))
                seen.add(a)


def min_coverage(distances, node, nodes_left):
    if not nodes_left:
        return 0
    return min([distances[node][other]
                + min_coverage(distances, other, nodes_left - {other}) for other in nodes_left])


def min_coverage_and_return(distances, node, nodes_left):
    if not nodes_left:
        return distances['0'][node]
    return min([distances[node][other]
                + min_coverage_and_return(distances, other, nodes_left - {other}) for other in nodes_left])


def calc_distances(grid, nodes):
    distances = defaultdict(dict)
    for a, b in combinations(nodes, 2):
        if b in distances[a]:
            continue
        dist, additionals = bfs(nodes[a], nodes[b], grid, nodes)
        distances[a][b] = dist
        distances[b][a] = dist
        for c, dist in additionals.items():
            distances[a][c] = dist
            distances[c][a] = dist
    return distances


grid = [l.rstrip() for l in open('./input.txt').readlines()]
items = read_items(grid)
distances = calc_distances(grid, items)

print(f"part 1: {min_coverage(distances, '0', set(items.keys()) - {'0'})}")
print(f"part 2: {min_coverage_and_return(distances, '0', set(items.keys()) - {'0'})}")
print(datetime.datetime.now() - begin_time)
