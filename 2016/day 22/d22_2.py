import datetime
import re
import showgrid
from collections import deque

from aopython import vector_add

begin_time = datetime.datetime.now()
sizes = []
useds = []
empty_pos = None
goal_pos = None
DIRS = [(0, 1), (0, -1), (-1, 0), (1, 0)]


def adjacents(pos):
    for npos in [vector_add(pos, d) for d in DIRS]:
        nx, ny = npos
        if 0 <= ny < len(sizes) and 0 <= nx < len(sizes[ny]):
            yield nx, ny


def bfs(start, end):
    q = deque([(*start, 0, [])])
    seen = set()
    while q:
        px, py, steps, path = q.popleft()
        fpos = (px, py)

        if fpos == end:
            return steps, path

        for ax, ay in adjacents((px, py)):
            if sizes[py][px] >= useds[ay][ax] and tuple([ax, ay]) not in seen:
                seen.add((ax, ay))
                q.append((ax, ay, steps+1, path + [(ax, ay)]))


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        if line.startswith('/dev/grid'):
            x, y, siz, used, *_ = list(map(int, re.findall(r'\d+', line)))
            if len(sizes) <= y:
                sizes.append([])
                useds.append([])

            sizes[y].append(siz)
            useds[y].append(used)
            if not used:
                empty_pos = (x, y)
    goal_pos = tuple([len(sizes[0]) - 1, 0])

# showgrid.pcolormesh([[v if v < 100 else 100 for v in row] for row in sizes])
# showgrid.pcolormesh([[v if v < 90 else 90 for v in row] for row in useds])

print(f'start {empty_pos} goal {goal_pos} goal size {useds[goal_pos[1]][goal_pos[0]]}')
# first move free one to Goal
steps, path = bfs(empty_pos, goal_pos)
print(f'{steps} steps to move empty slot to goal')

for px, py in path:
    ex, ey = empty_pos
    useds[ey][ex] = useds[py][px]
    empty_pos = (px, py)

goal_pos = path[-2]
print(f'new goal pos {goal_pos}')

# since max used space in both top rows is less than min free space in both rows...
assert max(useds[0] + useds[1]) < min(sizes[0] + sizes[1])
# ... we need to move the empty space (five steps) around the goal for each x we still need to move the goal
steps += (5 * goal_pos[0])
print(steps)
print(datetime.datetime.now() - begin_time)
