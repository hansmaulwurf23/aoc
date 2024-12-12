import datetime
from collections import defaultdict, deque
from aopython import vector_add

begin_time = datetime.datetime.now()
DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))


def in_grid(x, y):
    global DIMX, DIMY
    return 0 <= x < DIMX and 0 <= y < DIMY


def get_plant(x, y):
    global garden
    return garden[y][x] if in_grid(y, x) else '@'


def count_edges(orgfences, curplant):
    edges = 0
    fences = set(orgfences)
    while fences:
        cur = list(min(fences))
        in_out_offset = 0 if get_plant(cur[0], cur[1]) == curplant else 2
        edges += 1
        samedim = 0 if cur[0] == cur[2] else 1
        while tuple(cur) in fences and \
                get_plant(cur[0 + in_out_offset], cur[1 + in_out_offset]) == curplant:
            fences.remove(tuple(cur))
            cur[samedim] = cur[samedim] + 1
            cur[samedim + 2] = cur[samedim + 2] + 1

    return edges


def get_pot_fences(x, y):
    p = get_plant(x, y)
    pot_fences = set()
    for nxt in [vector_add((x, y), d) for d in DIRS]:
        if in_grid(*nxt) and get_plant(*nxt) != p or not in_grid(*nxt):
            nx, ny = nxt
            fx, tx, fy, ty = min(x, nx), max(x, nx), min(y, ny), max(y, ny)
            pot_fences.add((fx, fy, tx, ty))
    return pot_fences


def get_area_and_fences(start):
    q = deque()
    q.append(start)
    seen, pot_fences = {start}, set()

    while q:
        cur = q.popleft()
        x, y = cur
        curplant = get_plant(*cur)

        for nxt in [tuple(vector_add(cur, d)) for d in DIRS]:
            if nxt not in seen:
                if (in_grid(*nxt) and get_plant(*nxt) != curplant) or not in_grid(*nxt):
                    nx, ny = nxt
                    fx, tx, fy, ty = min(x, nx), max(x, nx), min(y, ny), max(y, ny)
                    pot_fences.add((fx, fy, tx, ty))
                if in_grid(*nxt) and get_plant(*nxt) == curplant:
                    q.append(nxt)
                    seen.add(nxt)

    return seen, pot_fences


def get_pot_count_and_fences():
    global garden
    pot_counter = defaultdict(list)
    pot_fences = defaultdict(list)
    todo = {(x, y) for y, l in enumerate(garden) for x, c in enumerate(l)}

    while todo:
        cur = todo.pop()
        p = get_plant(*cur)
        area, fences = get_area_and_fences(cur)
        pot_counter[p].append(len(area))
        pot_fences[p].append(fences)
        todo -= area

    return pot_counter, pot_fences


def cost(pot_counter, pot_fences):
    s1, s2 = 0, 0
    for p, pot_list in pot_counter.items():
        for counter, fences in zip(pot_list, pot_fences[p]):
            # print(p, counter, fences)
            s1 += counter * len(fences)
            # print(p, counter, count_edges(fences, p))
            s2 += counter * count_edges(fences, p)

    assert s1 in (1546338, 1930, 772, 692, 1184)
    assert s2 in (978590, 1206, 436, 236, 368)
    return s1, s2


with open('./input.txt') as f:
    garden = list(map(lambda l: l.rstrip(), f.readlines()))
    DIMX, DIMY = len(garden[0]), len(garden)

for i, x in enumerate(cost(*get_pot_count_and_fences())):
    print(f'part {i + 1}: {x}')
print(datetime.datetime.now() - begin_time)
