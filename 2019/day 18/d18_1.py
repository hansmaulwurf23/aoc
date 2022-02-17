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


def traverse_breadth_first(root, graph, doors, keysets, rest_keys):
    found_keysets = []
    q = deque()
    visited = set()
    visited.add(root)
    q.appendleft((root, 0, []))
    while len(q):
        node, steps, on_the_way_keys = q.pop()
        if node in key_loc_to_name and key_loc_to_name[node] in rest_keys:
            on_the_way_keys.append(key_loc_to_name[node])
            found_keysets.append((on_the_way_keys, node, steps))
        if node in keysets and keysets[node][0][0] in rest_keys:
            ks_keys, rtsteps, alt_end, altsteps = keysets[node]
            if ks_keys[0] in rest_keys:
                if alt_end and len(list(filter(lambda a: a not in visited and a not in doors, adjacent_list(alt_end, walls)))):
                    found_keysets.append((ks_keys, alt_end, steps + altsteps))
                else:
                    found_keysets.append((ks_keys, node, steps + rtsteps))
                for k in [keys[k] for k in ks_keys]:
                    visited.add(k)
            if alt_end:
                if alt_end not in visited:
                    visited.add(alt_end)
                    q.appendleft((alt_end, steps + altsteps, on_the_way_keys.copy()))

        for a, distance in graph[node]:
            if a in doors:
                continue
            if a not in visited:
                visited.add(a)
                q.appendleft((a, steps + distance, on_the_way_keys.copy()))

    return found_keysets


def adjacents(pos, walls):
    """generator for all adjacents (no wall!) of a given position"""
    for m in moves:
        a = tuple(vector_add(pos, m))
        if a not in walls:
            yield a


def adjacent_list(pos, walls, last_pos=None):
    """returns all adjacents of a given pos which are not wall and optional not the given last_pos"""
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


def possible_new_paths(cur_pos, graph, doors, keysets, rest_keys, collected_keys):
    return traverse_breadth_first(cur_pos, graph, apply_keys_to_doors(collected_keys, doors), keysets, rest_keys)


def get_key_door_dependencies(root, walls, doors, keys):
    q = deque()
    visited = set()
    visited.add(root)
    q.appendleft((root, 0, []))
    key_door_deps = defaultdict(list)
    while len(q):
        node, steps, on_the_way_doors = q.pop()
        adjs = adjacents(node, walls)
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
        names[key_loc_to_name[k_pos]] = tuple(map(lambda x: door_loc_to_name[x], deps))
        print(f'{key_loc_to_name[k_pos]} blocked by {names[key_loc_to_name[k_pos]]}')
    return names


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


def bfs(root, target, walls):
    q = deque()
    visited = set()
    visited.add(root)
    q.appendleft((root, 0))
    while len(q):
        node, steps = q.pop()
        adjs = adjacent_list(node, walls)

        if node == target:
            return steps

        for a in adjs:
            if a not in visited:
                visited.add(a)
                q.appendleft((a, steps + 1))

def calc_len(sequence):
    order = deque(sequence)
    root = order.popleft()
    root = keys[root] if root in keys else root
    steps = 0
    for target in map(lambda k: keys[k] if k in keys else k, order):
        steps += bfs(root, target, walls)
        root = target
        print(f'found {key_loc_to_name[target]} after {steps} steps')

    return steps



def generate_keysets(graph, doors, keys, key_door_deps):
    todos = defaultdict(list)
    for k, locking_doors in key_door_deps.items():
        if len(locking_doors):
            todos[locking_doors].append(k)

    last_door_loot = dict()

    # if multiple keys depend on a same set of doors
    for tododoors, todokeys in [(d, k) for d, k in todos.items() if len(k) > 1]:
        last_door = doors[tododoors[-1]]
        sum_steps = 0
        door_furhter_down = None
        q = deque()
        q.appendleft(last_door)
        visited = set()
        visited.add(last_door)
        while len(q):
            node = q.pop()
            for a, steps in graph[node]:
                if a not in visited:
                    if a in door_loc_to_name.keys():
                        if door_loc_to_name[a] not in tododoors:
                            door_furhter_down = a
                        continue
                    visited.add(a)
                    sum_steps += steps
                    q.appendleft(a)

        if door_furhter_down:
            # area of same door dependent keys is between two doors! we need to create two alternative ends
            # of this keys: last_door and the door that ended the loop. if keys in this set lie behind crossings
            # we must not calculate the steps twice (for the alternative going back).
            going_back_steps = 0
            for dead_end_key_pos in [keys[k] for k in todokeys if len(graph[keys[k]]) == 1]:
                last_pos = None
                while len(graph[dead_end_key_pos]) <= 2:
                    a, steps = next((a, steps) for a, steps in graph[dead_end_key_pos] if a != last_pos)
                    going_back_steps += steps
                    last_pos = dead_end_key_pos
                    dead_end_key_pos = a

            # last_door_loot[last_door] = (todokeys, sum_steps * 2, door_furhter_down, sum_steps + going_back_steps)
        else:
            # same door dependency keys in dead end area so collecting all and going back -> * 2
            last_door_loot[last_door] = (todokeys, sum_steps * 2, door_furhter_down, 0)
            print(f'keys frozen to set {todokeys} with door dependency {tododoors}: {last_door}->{last_door_loot[last_door]}')

    return last_door_loot


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

# showgrid.show_grid(walls, highlights={'r':doors.values(), 'y':keys.values()}, s=36)
dead_ends = get_dead_ends(walls, origin)
# showgrid.show_grid(walls, highlights={'r': dead_ends, 'violet':doors.values(), 'y':keys.values()}, s=36)
simplify_dead_ends(walls, dead_ends, set(keys.values()))
# showgrid.show_grid(walls, highlights={'r':doors.values(), 'y':keys.values()}, s=36)
# showgrid.show_grid(walls, highlights={'r':doors, 'b':keys}, s=36, minTicks=False, c='lightgrey', highlightsize=64)
# print(calc_len((origin, 'd', 'a', 'l', 'g', 'x', 'h', 'q', 'k', 'o', 's', 'w', 'j', 'b', 'm', 'z', 'f', 'c', 'r', 'v', 't', 'y', 'u', 'n', 'i', 'e', 'p')))
# exit(0)
key_door_deps = get_key_door_dependencies(origin, walls, set(doors.values()), set(keys.values()))
graph = generate_graph(origin, walls, set(keys.values()), set(doors.values()))
keysets = generate_keysets(graph, doors, keys, key_door_deps)
# showgrid.show_grid(list(graph.keys()) + [[0,0],[80,80]], s=36)


# state is current_steps, current_position, current_collected_keys
start_state = 0, tuple(origin), tuple()
pq = [start_state]
visited = set()
last_log = 0
log_master = ('d', 'a', 'l', 'g', 'x', 'h', 'q', 'k', 'o', 's', 'w', 'j', 'b', 'm', 'z', 'f', 'c', 'r', 'v', 't', 'y',
              'u', 'n', 'i', 'e', 'p')
while len(pq) > 0:
    cur_steps, cur_pos, collected_keys = heapq.heappop(pq)
    # if cur_steps > last_log + 100:
    #     print(cur_steps, len(collected_keys), collected_keys, len(pq))
    #     last_log = cur_steps

    if all([x == y for (x, y) in zip(collected_keys, log_master)]):
        print(cur_steps, len(collected_keys), cur_pos, collected_keys, len(pq))

    if collected_keys in visited:
        continue
    visited.add(collected_keys)

    rest_keys = tuple([k for k in keys.keys() if k not in collected_keys])
    if len(rest_keys) == 0:
        print(cur_steps)
        break

    for found_keys, last_pos, steps in possible_new_paths(cur_pos, graph, doors, keysets, rest_keys, collected_keys):
        # new_rest_keys = tuple(k for k in rest_keys if k not in found_keys)
        new_collected_keys = tuple(collected_keys) + tuple(found_keys)
        if new_collected_keys in visited:
            continue

        heapq.heappush(pq, (cur_steps + steps, last_pos, new_collected_keys))

print(cur_steps, cur_pos, collected_keys, rest_keys)
print('4424 <')
print('4456 <')
print(datetime.datetime.now() - begin_time)
