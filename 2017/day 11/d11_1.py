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
        cur_pos = vector_add(cur_pos, moves[step])
        path.append(cur_pos)

    return tuple(cur_pos)


def steps(pos):
    # return bfs((0, 0), pos)
    x, y = pos
    steps = abs(x)
    steps += (abs(y) - steps) // 2
    return steps


def bfs(root, target):
    q = deque()
    q.append((root, 0))
    seen = set()
    while True:
        cur_pos, steps = q.popleft()

        if cur_pos == target:
            return steps

        seen.add(cur_pos)

        for m in moves.values():
            if (d := tuple(vector_add(cur_pos, m))) not in seen:
                q.append((d, steps + 1))


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        final_pos = run_path(line)

assert steps(run_path('ne,ne,ne')) == 3
assert steps(run_path('ne,ne,sw,sw')) == 0
assert steps(run_path('ne,ne,s,s')) == 2
assert steps(run_path('se,sw,se,sw,sw')) == 3
print(f'final position {final_pos}')
print(steps(final_pos))
print(datetime.datetime.now() - begin_time)
