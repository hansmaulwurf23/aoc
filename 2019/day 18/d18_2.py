import datetime
import math
from collections import deque, defaultdict
import showgrid
from aopython import vector_add

begin_time = datetime.datetime.now()
moves = {(0, 1), (0, -1), (+1, 0), (-1, 0)}

walls = []
keys = dict()
doors = dict()
key_loc_to_name = dict()
door_loc_to_name = dict()
origin = None
cache = dict()
bfs_cache = dict()
rk_cache = dict()


def bfs(root, target):
    if (root, target) in bfs_cache:
        return bfs_cache[(root, target)]

    q = deque()
    visited = set()
    visited.add(root)
    q.appendleft((root, 0))
    while len(q):
        node, steps = q.pop()
        adjs = adjacents(node)

        if node == target:
            bfs_cache[(root, target)] = steps
            return steps

        for a in adjs:
            if a not in visited:
                visited.add(a)
                q.appendleft((a, steps + 1))


def adjacents(pos, last_pos=None):
    """returns all adjacents of a given pos which are not wall and optional not the given last_pos"""
    res = []
    for m in moves:
        x, y = tuple(vector_add(pos, m))
        if last_pos is not None and (x, y) == last_pos:
            continue
        if not walls[y][x]:
            res.append((x, y))

    return res


def get_dead_ends(root):
    """find all coordinates of dead ends"""
    q = deque()
    visited = set()
    visited.add(root)
    q.appendleft((root, 0))
    dead_ends = set()
    while len(q):
        proceeded = False
        node, steps = q.pop()
        adjs = adjacents(node)
        for i, a in enumerate(adjs):
            if a not in visited:
                proceeded = True
                visited.add(a)
                q.appendleft((a, steps + 1))

        if not proceeded and i == 0 and node != root:
            dead_ends.add(node)

    return dead_ends


def simplify_maze(walls, dead_ends, keys):
    """starting from all dead ends, go back as long as no key or crossing (multiple adjacents) are found and convert
    the way back to a wall """
    for d in dead_ends:
        if d in keys:
            continue
        x, y = tuple(d)
        while True:
            adjs = adjacents(d, (x, y))
            walls[y][x] = 1

            # stop at intersection
            if len(adjs) > 1:
                break

            x, y = tuple(d)
            d = adjs[0]
            # or at a key
            if d in keys:
                walls[y][x] = 1
                break


def get_key_door_dependencies(root, doors, keys):
    q = deque()
    visited = set()
    visited.add(root)
    q.appendleft((root, 0, []))
    key_door_deps = defaultdict(list)
    while len(q):
        node, steps, on_the_way_doors = q.pop()
        adjs = adjacents(node)
        for i, a in enumerate(adjs):
            if a not in visited:
                visited.add(a)
                if a in doors:
                    q.appendleft((a, steps + 1, on_the_way_doors + [a]))
                else:
                    q.appendleft((a, steps + 1, on_the_way_doors))
                if a in keys:
                    key_door_deps[a] += on_the_way_doors

    names = dict()
    for k_pos, deps in key_door_deps.items():
        names[key_loc_to_name[k_pos]] = set(map(lambda x: door_loc_to_name[x].lower(), deps))
        # print(f'{key_loc_to_name[k_pos]} needs keys {names[key_loc_to_name[k_pos]]}')
    return names


def reachable_keys(rest_keys, i):
    if (rest_keys, i) in rk_cache:
        return rk_cache[(rest_keys, i)]

    collected_keys = set([k for k in keys.keys() if k not in rest_keys])
    reachable = []
    for rk in rest_keys:
        if rk in key_requires_keys[i] and key_requires_keys[i][rk].issubset(collected_keys):
            reachable.append(rk)

    rk_cache[(rest_keys, i)] = reachable
    return reachable


def collect_rest_keys(cur_key_positions, rest_keys):
    if len(rest_keys) == 0:
        return 0

    if (cur_key_positions, rest_keys) in cache:
        return cache[(cur_key_positions, rest_keys)]

    result = math.inf
    for i, cur_key_pos in enumerate(cur_key_positions):
        for key in reachable_keys(rest_keys, i):
            new_key_positions = list(cur_key_positions)
            new_key_positions[i] = keys[key]
            d = bfs(cur_key_pos, keys[key]) + collect_rest_keys(tuple(new_key_positions), tuple([k for k in rest_keys if k != key]))
            result = min(result, d)

    cache[(cur_key_positions, rest_keys)] = result
    return result


with open('./input.txt') as f:
    y = 0
    while line := f.readline().rstrip():
        walls.append([])
        for x, c in enumerate(line):
            walls[y].append(1 if c == '#' else 0)
            if c == '@':
                center = (x, y)
            elif ord(c) in range(ord('a'), ord('z') + 1):
                keys[c] = (x, y)
                key_loc_to_name[(x, y)] = c
            elif ord(c) in range(ord('A'), ord('Z') + 1):
                doors[c] = (x, y)
                door_loc_to_name[(x, y)] = c

        y += 1

# part two modifications
origins = []
for dx, dy in [(1,1), (1,-1), (-1,1), (-1,-1)]:
    origins.append(tuple(vector_add(center, (dx, dy))))

simplify_maze(walls, get_dead_ends(center), set(keys.values()))

for ax, ay in adjacents(center):
    walls[ay][ax] = 1
walls[center[1]][center[0]] = 1

key_requires_keys = []
for origin in origins:
    key_requires_keys.append(get_key_door_dependencies(origin, set(doors.values()), set(keys.values())))

print(collect_rest_keys(tuple(origins), tuple(keys.keys())))
print(datetime.datetime.now() - begin_time)
