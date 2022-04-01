import datetime
from collections import deque

import showgrid
from aopython import vector_add

begin_time = datetime.datetime.now()

moves = {
    'n': (0, 2),
    'ne': (1, 1),
    'se': (1, -1),
    's': (0, -2),
    'sw': (-1, -1),
    'nw': (-1, 1)
}


def run_path(steps):
    cur_pos = (0, 0)
    path = [cur_pos]
    for step in steps.split(','):
        cur_pos = tuple(vector_add(cur_pos, moves[step]))
        path.append(cur_pos)

    return path


def max_steps(path):
    steps = max([abs(x) + ((abs(y) - abs(x)) // 2) for (x, y) in path])
    # assert bfs((0, 0), path) == max([abs(x) + ((abs(y) - abs(x)) // 2) for (x, y) in path])
    return steps


def bfs(root, path):
    targets = set(path)
    q = deque()
    q.append((root, 0))
    seen = set()
    while True:
        cur_pos, steps = q.popleft()

        if cur_pos in targets:
            targets.remove(cur_pos)
            print(len(targets), len(seen))
            if not targets:
                return steps
        seen.add(cur_pos)

        for m in moves.values():
            if (d := tuple(vector_add(cur_pos, m))) not in seen:
                q.append((d, steps + 1))


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        path = run_path(line)

print(max_steps(path))
print(datetime.datetime.now() - begin_time)
