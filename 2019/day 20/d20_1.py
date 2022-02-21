import datetime
from collections import deque

import showgrid
from aopython import vector_add

walls, portals = None, None
begin_time = datetime.datetime.now()


def get_walls(grid):
    res = set()
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == '#':
                res.add((x, y))

    return res


def get_portals(grid):
    parts = dict()
    portals = dict()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            c = grid[y][x]
            if 'A' <= c <= 'Z':
                if y < len(grid) - 1 and x < len(grid[y + 1]) and 'A' <= (d := grid[y + 1][x]) <= 'Z':
                    # vertical portal
                    key = c + d
                    coords = (x, y - 1) if y > 0 and grid[y - 1][x] == '.' else (x, y + 2)
                elif x < len(grid[y]) - 1 and 'A' <= (d := grid[y][x + 1]) <= 'Z':
                    # horizontal portal
                    key = c + d
                    coords = (x - 1, y) if grid[y][x - 1] == '.' else (x + 2, y)
                else:
                    # print(f'error reading portal! {(x, y, c)}')
                    walls.add((x, y))
                    continue

                if key not in parts:
                    parts[key] = coords
                else:
                    portals[coords] = parts[key]
                    portals[parts[key]] = coords
                    del parts[key]

                walls.add((x, y))

    return portals, parts['AA'], parts['ZZ']


def adjacents(pos):
    adjs = []
    for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        npos = tuple(vector_add(d, pos))
        if npos not in walls:
            adjs.append(npos)
    return adjs


def bfs(root, target):
    q = deque()
    # q.append((root, 0, [root]))
    q.append((root, 0))
    visited = set()
    while q:
        # node, steps, track = q.popleft()
        node, steps = q.popleft()

        if node == target:
            # showgrid.show_grid(walls, highlights={'lightgreen':track}, s=12, highlightsize=12, c='grey')
            return steps

        visited.add(node)

        if node in portals:
            if portals[node] not in visited:
                # print(f'jumping from {node} to {portals[node]}')
                # q.append((portals[node], steps + 1, track.copy() + [portals[node]]))
                q.append((portals[node], steps + 1))
                continue

        for a in adjacents(node):
            if a not in visited:
                # q.append((a, steps + 1, track.copy() + [a]))
                q.append((a, steps + 1))


with open('./input.txt') as f:
    grid = [list(l.rstrip('\n')) for l in f.readlines()]

walls = get_walls(grid)
portals, start_node, end_node = get_portals(grid)
print(bfs(start_node, end_node))
print(datetime.datetime.now() - begin_time)
