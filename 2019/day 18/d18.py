import datetime
import heapq
from collections import deque, defaultdict
import showgrid
from aopython import vector_add

begin_time = datetime.datetime.now()
moves = {(0, 1), (0, -1), (+1, 0), (-1, 0)}

walls = set()
keys = dict()
doors = dict()
key_loc_to_name = dict()
door_loc_to_name = dict()
origin = None
keysets = dict()


def traverse_breadth_first(start, collected_keys):
    q = deque()
    visited = set()
    visited.add(start)
    q.appendleft((start, 0))
    while len(q):
        node, steps = q.pop()
        if node in key_loc_to_name and key_loc_to_name[node] not in collected_keys:
            yield node, steps

        for a in adjacent_list(node):
            if a in doors and key_loc_to_name[a] not in collected_keys:
                continue
            if a not in visited:
                visited.add(a)
                q.appendleft((a, steps + 1))


def adjacents(pos, walls):
    """generator for all adjacents (no wall!) of a given position"""
    for m in moves:
        a = tuple(vector_add(pos, m))
        if a not in walls:
            yield a


def adjacent_list(pos, last_pos=None):
    """returns all adjacents of a given pos which are not wall and optional not the given last_pos"""
    res = []
    for m in moves:
        a = tuple(vector_add(pos, m))
        if last_pos is not None and a == last_pos:
            continue
        if a not in walls:
            res.append(a)

    return res


def get_dead_ends(walls, root):
    """find all coordinates of dead ends"""
    q = deque()
    visited = set()
    visited.add(root)
    q.appendleft((root, 0))
    dead_ends = set()
    while len(q):
        proceeded = False
        node, steps = q.pop()
        adjs = adjacents(node, walls)
        for i, a in enumerate(adjs):
            if a not in visited:
                proceeded = True
                visited.add(a)
                q.appendleft((a, steps + 1))

        if not proceeded and i == 0:
            dead_ends.add(node)

    return dead_ends


def simplify_dead_ends(walls, dead_ends, keys):
    """starting from all dead ends, go back as long as no key or crossing (multiple adjacents) are found and convert
    the way back to a wall """
    for d in dead_ends:
        if d in keys:
            continue
        last_pos = tuple(d)
        while True:
            adjs = adjacent_list(d, last_pos)
            walls.add(last_pos)

            if len(adjs) > 1:
                break

            last_pos = tuple(d)
            d = adjs[0]
            if d in keys:
                walls.add(last_pos)
                break

with open('./input.txt') as f:
    y = 0
    while line := f.readline().rstrip():
        for x, c in enumerate(line):
            if c == '#':
                walls.add((x, y))
            if c == '@':
                origin = (x, y)
            elif ord(c) in range(ord('a'), ord('z') + 1):
                keys[c] = (x, y)
                key_loc_to_name[(x, y)] = c
            elif ord(c) in range(ord('A'), ord('Z') + 1):
                doors[c] = (x, y)
                door_loc_to_name[(x, y)] = c

        y += 1

# found next set in earlier tries (with wrong result) and using this for debugging (see dijkstra and calc_len below)
# log_master = ('d', 'a', 'l', 'g', 'x', 'h', 'q', 'k', 'o', 's', 'j', 'm', 'z', 'f', 'c', 'r', 'v', 't', 'y', 'u', 'n', 'i', 'w', 'b', 'e', 'p')
# showgrid.show_grid(walls, highlights={'r':doors.values(), 'y':keys.values()}, s=36)
dead_ends = get_dead_ends(walls, origin)
# showgrid.show_grid(walls, highlights={'r': dead_ends, 'violet':doors.values(), 'y':keys.values()}, s=36)
simplify_dead_ends(walls, dead_ends, set(keys.values()))
# showgrid.show_grid(walls, highlights={'r':doors.values(), 'y':keys.values()}, s=36)
# showgrid.show_grid(walls, highlights={'r':doors, 'b':keys}, s=36, minTicks=False, c='lightgrey', highlightsize=64)
# showgrid.show_grid(list(graph.keys()) + [[0,0],[80,80]], s=36)


# state is current_steps, current_position, current_collected_keys
start_state = 0, tuple(origin), tuple()
pq = [start_state]
visited = set()
last_log = 0

while len(pq) > 0:
    cur_steps, cur_pos, collected_keys = heapq.heappop(pq)
    if cur_steps > last_log + 25:
        print(cur_steps, len(collected_keys), collected_keys, len(pq))
        last_log = cur_steps

    # if all([x == y for (x, y) in zip(collected_keys, log_master)]):
    #     print(cur_steps, len(collected_keys), cur_pos, collected_keys, len(pq))

    if collected_keys in visited:
        continue
    visited.add((cur_pos, collected_keys))

    if len(collected_keys) == len(keys):
        print(cur_steps)
        break

    for last_pos, steps in traverse_breadth_first(cur_pos, collected_keys):
        # new_rest_keys = tuple(k for k in rest_keys if k not in found_keys)
        new_collected_keys = tuple(collected_keys) + tuple([key_loc_to_name[last_pos]])
        if (last_pos, new_collected_keys) in visited:
            continue

        heapq.heappush(pq, (cur_steps + steps, last_pos, new_collected_keys))

print(cur_steps, cur_pos, collected_keys)
print('4388')
print('4424 <')
print('4456 <')
print('4420 ?!')
print(datetime.datetime.now() - begin_time)
