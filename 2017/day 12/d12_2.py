import datetime
import re
from collections import defaultdict

begin_time = datetime.datetime.now()
connections = defaultdict(set)


def reachables(connections, id):
    ids = set()
    q = [id]
    while q:
        cur_id = q.pop()
        ids.add(cur_id)

        for c in connections[cur_id]:
            if c not in ids:
                q.append(c)
    return ids


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        ids = list(map(int, re.findall(r'\d+', line)))
        connections[ids[0]] |= set(ids[1:])

groups = []
todos = set(connections.keys())
while todos:
    grp = reachables(connections, todos.pop())
    todos -= grp
    groups.append(grp)

print(len(groups))
print(datetime.datetime.now() - begin_time)
