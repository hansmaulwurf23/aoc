import datetime

from aopython import vector_add, manhattan_distance, vector, vector_sgn

begin_time = datetime.datetime.now()

DIRS = {'D': (0, -1), 'U': (0, 1), 'L': (-1, 0), 'R': (1, 0)}
head = (0, 0)
tail = (0, 0)
visited = {(0, 0)}

with open('./input.txt') as f:
    while line := f.readline().rstrip():
        head_dir, steps = line.split(' ')
        steps = int(steps)
        for step in range(steps):
            head = tuple(vector_add(head, DIRS[head_dir]))
            mh_dist = manhattan_distance(head, tail)
            same_axis = (head[0] == tail[0] or head[1] == tail[1])
            if 0 <= mh_dist <= 1:
                # adjacent
                continue
            elif mh_dist == 2:
                if same_axis:
                    v = vector_sgn(vector(tail, head))
                    tail = tuple(vector_add(tail, v))
                    visited.add(tail)
                else:
                    # diagonally adjacent
                    continue
            else:
                v = vector(tail, head)
                direction = [v[0] // abs(v[0]), v[1] // abs(v[1])]
                tail = tuple(vector_add(tail, direction))
                visited.add(tail)

print(len(visited))
print(datetime.datetime.now() - begin_time)
