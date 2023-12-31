import datetime
from collections import defaultdict, deque
from itertools import combinations

begin_time = datetime.datetime.now()

network = defaultdict(set)
connections = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        elem, conns = line.split(': ')
        for con in conns.split():
            network[elem].add(con)
            network[con].add(elem)
            connections.append((min(elem, con), max(elem, con)))

def bfs(start, end, used_edges):
    global network
    previous_node = {start: None}
    queue = [start]
    while queue:
        node = queue.pop()

        if node == end:
            reverse_path = []
            while node != start:
                reverse_path.append((previous_node[node], node))
                node = previous_node[node]
            return list(reversed(reverse_path))

        for other in network[node]:
            if other not in previous_node and (node, other) not in used_edges:
                previous_node[other] = node
                queue.append(other)

    return None

def find_paths(start, end):
    global network
    used_edges = set()
    distinct_paths = 0

    while True:
        path = bfs(start, end, used_edges)

        if path is None:
            return distinct_paths, used_edges

        distinct_paths += 1
        if distinct_paths > 3:
            return distinct_paths, used_edges
        used_edges |= set(path)


def get_reachables(start, used_edges):
    global network
    q = deque([start])
    seen = {start}
    while q:
        node = q.popleft()
        for other in network[node]:
            if other in seen:
                continue
            if (node, other) not in used_edges:
                seen.add(other)
                q.append(other)

    return seen


for node, other in combinations(network, 2):
    distinct_paths, used_edges = find_paths(node, other)
    if distinct_paths == 3:
        break
else:
    print('no solution')
    exit(0)

partition = get_reachables(node, used_edges)
partlen = len(partition)
p1 = partlen * (len(network) - partlen)
print(p1)
assert p1 == 619225
print(datetime.datetime.now() - begin_time)
