import datetime
from collections import defaultdict, deque

import showgrid
from aopython import vector_add

begin_time = datetime.datetime.now()

N, E, S, W = range(4)
dirs = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
invdir = {N: S, W: E, E: W, S: N}
moves = {N: (0, 1), E: (1, 0), S: (0, -1), W: (-1, 0)}

rooms = defaultdict(lambda: [None] * 4)

def bfs_max(rooms, root):
    q = deque()
    q.append((root, 0))
    visited = set()
    while q:
        node, steps = q.popleft()
        visited.add(node)

        for a in rooms[node]:
            if a is not None and a not in visited:
                q.append((a, steps + 1))

    return steps


def build_rooms(input, cur_pos):
    # print(len(rooms))
    while input:
        nxt = input.popleft()
        if nxt in dirs:
            cur_dir = dirs[nxt]
            next_pos = tuple(vector_add(cur_pos, moves[cur_dir]))
            rooms[cur_pos][cur_dir] = next_pos
            rooms[next_pos][invdir[cur_dir]] = cur_pos
            cur_pos = next_pos
        elif nxt == '(':
            parts = [[]]
            depth = 0
            while input:
                nxt = input.popleft()
                if nxt == ')':
                    if depth == 0:
                        break
                    else:
                        depth -= 1
                        parts[-1].append(nxt)
                elif nxt == '(':
                    depth += 1
                    parts[-1].append(nxt)
                elif nxt == '|' and depth == 0:
                    parts.append([])
                else:
                    parts[-1].append(nxt)

            # print(f"found this parts: {parts}")
            if list(filter(lambda l: len(l) == 0, parts)):
                for p in parts:
                    if len(p):
                        build_rooms(deque(p), tuple(cur_pos))
            else:
                for p in parts:
                    build_rooms(deque(p + list(input)), tuple(cur_pos))
                return

with open('./input.txt') as f:
    build_rooms(deque(f.readlines()[0].rstrip()[1:-1]), (0, 0))
print(f'build {len(rooms)} rooms.')
print(bfs_max(rooms, (0, 0)))
print(datetime.datetime.now() - begin_time)
