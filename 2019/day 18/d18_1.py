import datetime
import heapq
from collections import deque, defaultdict
import showgrid
from aopython import vector_add

begin_time = datetime.datetime.now()
moves = { (0, 1), (0, -1), (+1, 0), (-1, 0) }

walls = set()
keys = dict()
doors = dict()
key_loc_to_name = dict()
origin = None

def traverse_breadth_first(root, graph, doors, keys):
    found_keys = []
    q = deque()
    visited = set()
    visited.add(root)
    q.appendleft((root, 0))
    while len(q):
        node, steps = q.pop()
        if node in key_loc_to_name and key_loc_to_name[node] in keys:
            found_keys.append((node, steps))
        for a, distance in graph[node]:
            if a in doors:
                continue
            if a not in visited:
                visited.add(a)
                q.appendleft((a, steps + distance))

    return found_keys


def adjacents(pos, walls):
    for m in moves:
        a = tuple(vector_add(pos, m))
        if a not in walls:
            yield a


def adjacent_list(pos, walls, last_pos=None):
    res = []
    for m in moves:
        a = tuple(vector_add(pos, m))
        if last_pos is not None and a == last_pos:
            continue
        if a not in walls:
            res.append(a)

    return res


def apply_keys_to_doors(collected_keys, doors):
    res = set()
    for door_name, door_coords in doors.items():
        if door_name.lower() not in collected_keys:
            res.add(door_coords)

    return res


def possible_new_paths(cur_pos, graph, doors, keys, collected_keys):
    new_paths = []
    found_keys = traverse_breadth_first(cur_pos, graph, apply_keys_to_doors(collected_keys, doors), keys)
    for key_coords, steps in found_keys:
        new_paths.append((steps, key_coords))

    return new_paths


def get_key_door_dependencies(root, walls, doors, keys):
    q = deque()
    visited = set()
    visited.add(root)
    q.appendleft((root, 0, set()))
    key_door_deps = defaultdict(set)
    while len(q):
        node, steps, on_the_way_doors = q.pop()
        adjs = adjacents(node, walls)
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


# given the dead ends, go back as long as no gem (doors or keys) or crossing (multiple adjacents) are found
# and make convert the way back to a wall
def process_dead_ends(walls, dead_ends, keys):
    for d in dead_ends:
        if d in keys:
            continue
        last_pos = tuple(d)
        while True:
            adjs = adjacent_list(d, walls, last_pos)
            walls.add(last_pos)

            if len(adjs) > 1:
                break

            last_pos = tuple(d)
            d = adjs[0]
            if d in keys:
                walls.add(last_pos)
                break


def generate_graph(root, walls, keys, doors):
    graph = defaultdict(set)
    q = deque()
    visited = set()
    visited.add(root)
    q.appendleft((root, 0, root))
    while len(q):
        node, steps, last_waypoint = q.pop()
        adjs = adjacent_list(node, walls)

        if node in keys or node in doors or len(adjs) > 2:
            graph[node].add((last_waypoint, steps))
            graph[last_waypoint].add((node, steps))
            last_waypoint = node
            steps = 0

        for a in adjs:
            if a not in visited:
                visited.add(a)
                q.appendleft((a, steps + 1, last_waypoint))

    return graph


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
# showgrid.show_grid(walls, highlights={'r':doors.values(), 'y':keys.values()}, s=36)
key_door_deps = get_key_door_dependencies(origin, walls, set(doors.values()), set(keys.values()))
graph = generate_graph(origin, walls, set(keys.values()), set(doors.values()))
# showgrid.show_grid(list(graph.keys()) + [[0,0],[80,80]], s=36)


# state is current_steps, current_position, current_collected_keys, rest_keys
start_state = 0, tuple(origin), tuple(), tuple(keys.keys())
pq = [start_state]
visited = set()
last_log = 0
while len(pq) > 0:
    cur_steps, cur_pos, collected_keys, rest_keys = heapq.heappop(pq)
    if cur_steps > last_log + 100:
        print(cur_steps, len(collected_keys), collected_keys, len(pq))
        last_log = cur_steps

    if collected_keys in visited:
        continue
    visited.add(collected_keys)

    if len(rest_keys) == 0:
        print(cur_steps)
        break

    for steps, key_pos in possible_new_paths(cur_pos, graph, doors, rest_keys, collected_keys):
        collected_key = key_loc_to_name[key_pos]
        new_rest_keys = list(rest_keys)
        new_rest_keys.remove(collected_key)

        new_collected_keys = tuple(collected_keys + tuple(collected_key))
        if new_collected_keys in visited:
            continue

        heapq.heappush(pq, (cur_steps + steps, key_pos, new_collected_keys, new_rest_keys))


print('4456 <')
print(datetime.datetime.now() - begin_time)