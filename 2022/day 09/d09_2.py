import datetime

import showgrid
from aopython import vector_add, manhattan_distance, vector, vector_sgn

begin_time = datetime.datetime.now()

DIRS = {'D': (0, -1), 'U': (0, 1), 'L': (-1, 0), 'R': (1, 0)}
rope = []
TAIL = 9
for k in range(10):
    rope.append((0, 0))
visited = {(0, 0)}

with open('./input.txt') as f:
    while line := f.readline().rstrip():
        head_dir, steps = line.split(' ')
        steps = int(steps)
        # showgrid.show_grid(rope)
        for step in range(steps):
            rope[0] = tuple(vector_add(rope[0], DIRS[head_dir]))

            for k in range(1, len(rope)):
                pred = rope[k - 1]
                succ = rope[k]
                mh_dist = manhattan_distance(pred, succ)
                same_axis = (pred[0] == succ[0] or pred[1] == succ[1])
                if 0 <= mh_dist <= 1:
                    # adjacent
                    continue
                elif mh_dist == 2:
                    if same_axis:
                        v = vector_sgn(vector(succ, pred))
                        rope[k] = tuple(vector_add(succ, v))
                        if k == TAIL:
                            visited.add(rope[k])
                    else:
                        # diagonally adjacent
                        continue
                else:
                    v = vector(succ, pred)
                    direction = [v[0] // abs(v[0]), v[1] // abs(v[1])]
                    rope[k] = tuple(vector_add(succ, direction))
                    if k == TAIL:
                        visited.add(rope[k])

# showgrid.show_grid(rope)
# showgrid.show_grid(visited)
print(len(visited))
print(datetime.datetime.now() - begin_time)
