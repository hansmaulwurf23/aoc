import datetime
import heapq
from collections import deque, defaultdict
import showgrid
from aopython import vector_add

begin_time = datetime.datetime.now()
moves = { (0, 1), (0, -1), (+1, 0), (-1, 0) }

walls = set()
keys = dict()
key_loc_to_name = dict()
doors = dict()
origin = None
adj_cache = defaultdict(set)

def traverse_breadth_first(root, walls, doors, keys):
    found_gems = []
    q = deque()
    visited = set()
    visited.add(root)
    q.appendleft((root, 0))
    while len(q):
        node, steps = q.pop()
        if node in keys:
            found_gems.append((node, steps))
        for a, distance in adjacents(node, walls):
            if a in doors:
                continue
            if a not in visited:
                visited.add(a)
                q.appendleft((a, steps + distance))

    return found_gems


def adjacents(pos, walls):
    if pos in shortcuts:
        return tuple([shortcuts[pos]])

    res = []
    for m in moves:
        a = tuple(vector_add(pos, m))
        if a not in walls:
            res.append((a, 1))

    return res


def raw_adjacents(pos, walls):
    for m in moves:
        a = tuple(vector_add(pos, m))
        if a not in walls:
            yield a


def next_pos_list(pos, walls, last_pos):
    res = []
    for m in moves:
        a = tuple(vector_add(pos, m))
        if a not in walls and a != last_pos:
            res.append(a)

    return res


def apply_keys_to_doors(collected_keys, doors):
    res = set()
    for door_name, door_coords in doors.items():
        if door_name.lower() not in collected_keys:
            res.add(door_coords)

    return res


def possible_new_paths(cur_pos, doors, keys, collected_keys):
    new_paths = []
    found_keys = traverse_breadth_first(cur_pos, walls, apply_keys_to_doors(collected_keys, doors), set(keys.values()))
    for key_coords, steps in found_keys:
        new_paths.append((steps, key_coords, key_loc_to_name[key_coords]))

    return new_paths


def get_key_door_dependencies(root, walls, doors, keys):
    q = deque()
    visited = set()
    visited.add(root)
    q.appendleft((root, 0, set()))
    key_door_deps = defaultdict(set)
    while len(q):
        node, steps, on_the_way_doors = q.pop()
        adjs = raw_adjacents(node, walls)
        for i, a in enumerate(adjs):
            if a not in visited:
                visited.add(a)
                if a in doors:
                    q.appendleft((a, steps + 1, set(on_the_way_doors | set([a]))))
                else:
                    q.appendleft((a, steps + 1, on_the_way_doors))
                if a in keys:
                    key_door_deps[a] |= on_the_way_doors

    return key_door_deps


# find all coords of dead ends
def get_dead_ends(walls, root):
    q = deque()
    visited = set()
    visited.add(root)
    q.appendleft((root, 0))
    dead_ends = set()
    while len(q):
        proceeded = False
        # i = 0
        node, steps = q.pop()
        adjs = raw_adjacents(node, walls)
        for i, a in enumerate(adjs):
            if a not in visited:
                proceeded = True
                visited.add(a)
                q.appendleft((a, steps + 1))

        if not proceeded and i == 0:
            dead_ends.add(node)

    return dead_ends


# given the dead ends, go back as long as no gem (doors or keys) or crossing (multiple adjacents) are found
# and make convert the way back to a wall
def process_dead_ends(walls, dead_ends, keys):
    for d in dead_ends:
        if d in keys:
            continue
        last_pos = tuple(d)
        while True:
            adjs = next_pos_list(d, walls, last_pos)
            walls.add(last_pos)

            if len(adjs) > 1:
                break

            last_pos = tuple(d)
            d = adjs[0]
            if d in keys:
                walls.add(last_pos)
                break


def generate_shortcuts(walls, dead_ends, keys, doors):
    shortcuts = defaultdict(set)
    for d in [d for d in dead_ends if d in keys]:
        cur_key = d
        last_pos = tuple(d)
        start_pos = tuple(d)
        steps = 0
        while True:
            adjs = next_pos_list(d, walls, last_pos)

            if len(adjs) > 1:
                shortcuts[last_pos].add((start_pos, steps - 1))
                shortcuts[start_pos].add((last_pos, steps - 1))
                break

            last_pos = tuple(d)
            d = adjs[0]
            steps += 1
            if d in keys or d in doors:
                shortcuts[last_pos].add((start_pos, steps - 1))
                shortcuts[start_pos].add((last_pos, steps - 1))
                start_pos = tuple(d)
                steps = 0

    return shortcuts


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

        y += 1


# showgrid.show_grid(walls, highlights={'r':doors.values(), 'y':keys.values()}, s=36)

dead_ends = get_dead_ends(walls, origin)
# showgrid.show_grid(walls, highlights={'r': dead_ends, 'violet':doors.values(), 'y':keys.values()}, s=36)
process_dead_ends(walls, dead_ends, set(keys.values()))
showgrid.show_grid(walls, highlights={'r':doors.values(), 'y':keys.values()}, s=36)
key_door_deps = get_key_door_dependencies(origin, walls, set(doors.values()), set(keys.values()))

dead_ends = get_dead_ends(walls, origin)
shortcuts = generate_shortcuts(walls, dead_ends, set(keys.values()), set(doors.values()))



# state is current_steps, current_position, current_collected_keys, rest_keys
start_state = 0, tuple(origin), tuple(), keys.copy()
pq = [start_state]
visited = set()
while len(pq) > 0:
    cur_steps, cur_pos, collected_keys, rest_keys = heapq.heappop(pq)
    # if (len(collected_keys) > 12):
    print(cur_steps, len(collected_keys), collected_keys)

    # performance gain tests
    if cur_steps > 700:
        print('0:00:09.820945')
        break

    if collected_keys in visited:
        continue
    visited.add(collected_keys)

    # cost[cur_pos] = cur_steps
    if len(rest_keys) == 0:
        print(cur_steps)
        break

    for next_state in possible_new_paths(cur_pos, doors, rest_keys, collected_keys):
        steps, pos, collected_key = next_state
        new_rest_keys = rest_keys.copy()
        del new_rest_keys[collected_key]

        new_collected_keys = tuple(collected_keys + tuple(collected_key))
        if new_collected_keys in visited:
            continue

        # breadcrumbs[next_state[1]] = cur_apods
        heapq.heappush(pq, (cur_steps + steps, pos, new_collected_keys, new_rest_keys))


print('4456 <')
print(datetime.datetime.now() - begin_time)
