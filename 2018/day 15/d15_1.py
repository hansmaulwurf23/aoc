import datetime
from collections import namedtuple, defaultdict, deque
from itertools import product

from aopython import vector_add

begin_time = datetime.datetime.now()

Unit = namedtuple('Unit', ['HP', 'AP'])
elves = dict()
goblins = dict()
walls = set()

def unit_turn(u, allies, targets):
    target = None
    possible_moves = {}
    for t in sorted(targets.keys()):
        if is_adjacent(u, t) and (target is None or targets[target].HP > targets[t].HP):
            target = t

        possible_moves |= set(adjacents(t, only_free_space=True))

    # no target is immediately adjacent -> move move ya!
    if not target and possible_moves:
        pass

    if target:
        targets[target].HP -= allies[u].AP
        if targets[target].HP <= 0:
            del targets[target]


def combat_round():
    # all uni coordinates in reading order
    unit_coords = sorted(list(elves.keys()) + list(goblins.keys()))
    for u in unit_coords:
        targets = goblins if u in elves else elves
        unit_turn(u, targets)


def nearest_target(root, targets):
    q = deque()
    visited = set()
    visited.add(root)
    q.appendleft((root, 0))
    found = []
    min_distance = None
    while q:
        node, steps = q.pop()
        adjs = adjacents(node)

        if node in targets:
            found.append((node, steps))

        # cannot be better?
        if min_distance is not None and min_distance <= steps:
            continue

        for a in adjs:
            if a not in visited:
                visited.add(a)
                q.appendleft((a, steps + 1))

    target, steps = min(found, key=found.get(0))
    return target, steps


def is_adjacent(a, b):
    ax, ay = a
    bx, by = b
    return (ax == bx and (ay + 1 == by or ay - 1 == by)) or \
           (ay == by and (ax + 1 == bx or ax - 1 == bx))


def adjacents(pos, only_free_space=False):
    res = []
    for m in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        x, y = tuple(vector_add(pos, m))
        if only_free_space and ((y, x) in elves or (y, x) in goblins):
            continue
        if (y, x) not in walls:
            res.append((x, y))

    return res


with open('./input.txt') as f:
    y = 0
    while line := f.readline().rstrip():
        for x, c in enumerate(line):
            if c == '#':
                walls.add((y, x))
            elif c == 'G':
                goblins[(y, x)] = Unit(HP=300, AP=3)
            elif c == 'E':
                elves[(y, x)] = Unit(HP=300, AP=3)

            y += 1

print(datetime.datetime.now() - begin_time)
