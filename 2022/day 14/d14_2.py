import datetime
import showgrid
from aopython import vector_sgn, vector, vector_add

begin_time = datetime.datetime.now()
rocks = set()
sand = set()
DOWN, DOWN_LEFT, DOWN_RIGHT = (0, 1), (-1, 1), (1, 1)
MOVES = [DOWN, DOWN_LEFT, DOWN_RIGHT]
deepest_y = None


def run_sand():
    cur = (500, 0)
    while cur[1] < deepest_y + 1:
        for move in MOVES:
            next = tuple(vector_add(cur, move))
            if next in rocks or next in sand:
                continue
            else:
                cur = next
                break

        if cur != next:
            sand.add(cur)
            return cur != (500, 0)

    sand.add(cur)
    return cur != (500, 0)


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        straights = line.split(' -> ')
        s, end = 0, None
        for s in range(len(straights)):
            if s == 0:
                start = tuple(map(int, straights[s].split(',')))
                rocks.add(start)
                continue
            elif end is not None:
                start = end
            end = tuple(map(int, straights[s].split(',')))
            if deepest_y is None or end[1] > deepest_y:
                deepest_y = end[1]
            d = vector_sgn(vector(start, end))
            while start != end:
                start = tuple(vector_add(start, d))
                rocks.add(start)

while True:
    if not run_sand():
        break

print(len(sand))
print(datetime.datetime.now() - begin_time)
