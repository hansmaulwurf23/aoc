import datetime
import functools
from collections import deque

from aopython import vector_add

begin_time = datetime.datetime.now()
N, E, S, W = range(4)
DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))

# fav_no, start, end = 10, (1, 1), (7, 4)
fav_no, start, end = 1364, (1, 1), (31, 39)


@functools.cache
def is_wall(x, y):
    global fav_no
    r = x * x + 3 * x + 2 * x * y + y + y * y + fav_no
    return sum([int(d) for d in bin(r)[2:]]) % 2 == 1

@functools.cache
def adjacents(pos):
    for new_pos in [tuple(vector_add(d, pos)) for d in DIRS]:
        x, y = new_pos
        if x < 0 or y < 0:
            continue
        if is_wall(x, y):
            continue
        yield new_pos


def bfs(start, end):
    q = deque([(0, start)])
    seen = set()
    seen50 = set()
    while q:
        steps, pos = q.popleft()

        if pos == end:
            return steps, len(seen50)

        seen.add(pos)
        if steps <= 50:
            seen50.add(pos)

        for a in adjacents(pos):
            if a not in seen:
                q.append((steps + 1, a))


print(bfs(start, end))
print(datetime.datetime.now() - begin_time)
