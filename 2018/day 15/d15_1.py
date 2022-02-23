import datetime
import math
from collections import namedtuple, defaultdict, deque
from itertools import product

import showgrid
from aopython import vector_add

begin_time = datetime.datetime.now()

Unit = namedtuple('Unit', ['HP', 'AP'])
elves = dict()
goblins = dict()
walls = set()


def unit_turn(u, allies, targets):
    target = None
    possible_moves = set()
    for t in sorted(targets.keys()):
        if is_adjacent(u, t) and (target is None or targets[target].HP > targets[t].HP):
            target = t

        possible_moves |= set(adjacents(t, only_free_space=True))

    # no target is immediately adjacent -> move move ya!
    if not target and possible_moves:
        move_target, *_ = nearest_target(u, possible_moves)
        if move_target is None:
            # cannot move and have no target -> my turn is done
            return

        new_pos = step_to(u, move_target)
        allies[new_pos] = allies[u]
        del allies[u]
        u = new_pos
        if is_adjacent(u, move_target):
            target = move_target

    if target:
        targets[target].HP -= allies[u].AP
        if targets[target].HP <= 0:
            del targets[target]


def combat_round():
    # all uni coordinates in reading order
    unit_coords = sorted(list(elves.keys()) + list(goblins.keys()), key=lambda t: (t[1], t[0]))
    for u in unit_coords:
        allies, targets = (elves, goblins) if u in elves else (goblins, elves)
        unit_turn(u, allies, targets)


def step_to(root, target):
    if root[0] == target[0]:
        d = (0, 1) if target[1] > root[1] else (0, -1)
    elif root[1] == target[1]:
        d = (1, 0) if target[0] > root[0] else (-1, 0)
    else:
        # FIXME move vertically or horizontally first?
        d = (0, 1) if target[1] > root[1] else (0, -1)

    return tuple(vector_add(root, d))


def nearest_target(root, targets):
    q = deque()
    visited = set()
    visited.add(root)
    q.appendleft((root, 0))
    found = []
    min_distance = math.inf
    while q:
        node, steps = q.pop()

        if node in targets and min_distance >= steps:
            found.append((node, steps))
            min_distance = steps
            continue

        # cannot be better?
        if min_distance <= steps:
            continue

        for a in adjacents(node):
            if (a in elves or a in goblins) and a not in targets:
                continue
            if a not in visited:
                visited.add(a)
                q.appendleft((a, steps + 1))

    if found:
        target, steps = min(found, key=lambda f: (f[0][1], f[0][0]))
        return target, steps
    else:
        return None, None


def is_adjacent(a, b):
    ax, ay = a
    bx, by = b
    return (ax == bx and (ay + 1 == by or ay - 1 == by)) or \
           (ay == by and (ax + 1 == bx or ax - 1 == bx))


def adjacents(pos, only_free_space=False):
    res = []
    for m in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        x, y = tuple(vector_add(pos, m))
        if only_free_space and ((x, y) in elves or (x, y) in goblins):
            continue
        if (x, y) not in walls:
            res.append((x, y))

    return res


with open('./input.txt') as f:
    y = 0
    while line := f.readline().rstrip():
        for x, c in enumerate(line):
            if c == '#':
                walls.add((x, y))
            elif c == 'G':
                goblins[(x, y)] = Unit(HP=300, AP=3)
            elif c == 'E':
                elves[(x, y)] = Unit(HP=300, AP=3)

        y += 1

# showgrid.show_grid(walls, {'g': elves.keys(), 'r': goblins.keys()})
combat_round()
showgrid.show_grid(walls, {'g': elves.keys(), 'r': goblins.keys()})
print(datetime.datetime.now() - begin_time)
