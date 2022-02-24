import datetime
from collections import deque, defaultdict

import showgrid
from aopython import vector_add, min_max_2d

walls, portals = None, None
portal_names = dict()
begin_time = datetime.datetime.now()


def plot_max_w_portals(walls, portals):
    plot = defaultdict(set)
    for snode, target in portals.items():
        tnode, ldelta = target
        plot['g' if ldelta < 0 else 'r'].add(snode)
    showgrid.show_grid(walls, highlights=plot, s=12)


def get_walls(grid):
    res = set()
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == '#':
                res.add((x, y))

    return res


def get_portals(grid):
    wfx, wtx, wfy, wty = min_max_2d(walls)
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

                cx, cy = coords
                # level delta is -1 if x or y of portal coords is on outer wall boundaries
                lvl_delta = -1 if cx in [wfx, wtx] or cy in [wfy, wty] else 1
                if key not in parts:
                    parts[key] = (coords, lvl_delta)
                    portal_names[coords] = key
                else:
                    portals[coords] = (parts[key][0], lvl_delta)
                    portal_names[coords] = key
                    portals[parts[key][0]] = (coords, parts[key][1])
                    del parts[key]

                walls.add((x, y))

    # plot_max_w_portals(walls, portals)

    return portals, parts['AA'][0], parts['ZZ'][0]


def adjacents(pos, last_pos=None):
    adjs = []
    for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        npos = tuple(vector_add(d, pos))
        if last_pos is not None and npos == last_pos:
            continue
        if npos not in walls:
            adjs.append(npos)
    return adjs


def bfs(root, target):
    q = deque()
    q.append((root, 0, []))
    visited = set()
    while q:
        node, steps, portal_path = q.popleft()

        if node == target:
            print(portal_path)
            return steps

        visited.add(node)

        ncoords, level = node
        if ncoords in portals:
            new_coords, lvl_delta = portals[ncoords]
            new_level = level + lvl_delta
            if new_level >= 0 and (new_coords, new_level) not in visited:
                q.append(((new_coords, new_level), steps + 1, portal_path.copy() + [f'{portal_names[ncoords]}{level}']))
                # print(f'jumping from {ncoords} ({level}) to {new_coords} ({new_level})')
                continue

        for a in adjacents(ncoords):
            if (a, level) not in visited:
                q.append(((a, level), steps + 1, portal_path))


def get_dead_ends(root, end_node):
    """find all coordinates of dead ends"""
    q = deque()
    visited = set()
    visited.add(root)
    q.appendleft(root)
    dead_ends = set()
    while len(q):
        proceeded = False
        node = q.pop()
        if node in portals:
            if portals[node][0] not in visited:
                visited.add(portals[node][0])
                q.append(portals[node][0])
                continue

        adjs = adjacents(node)
        for i, a in enumerate(adjs):
            if a not in visited:
                proceeded = True
                visited.add(a)
                q.appendleft(a)

        if not proceeded and i == 0 and node != end_node:
            dead_ends.add(node)

    return dead_ends


def simplify_dead_ends(walls, dead_ends):
    """starting from all dead ends, go back as long as no key or crossing (multiple adjacents) are found and convert
    the way back to a wall """
    print(f'simplifying {len(dead_ends)} dead ends')
    for d in dead_ends:
        last_pos = tuple(d)
        while True:
            adjs = adjacents(d, last_pos)
            walls.add(last_pos)

            if len(adjs) > 1:
                break

            last_pos = tuple(d)
            d = adjs[0]


with open('./input.txt') as f:
    grid = [list(l.rstrip('\n')) for l in f.readlines()]

walls = get_walls(grid)
portals, start_node, end_node = get_portals(grid)
simplify_dead_ends(walls, get_dead_ends(start_node, end_node))
plot_max_w_portals(walls, portals)

print(bfs((start_node, 0), (end_node, 0)))
print(datetime.datetime.now() - begin_time)
