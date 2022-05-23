import datetime

from aopython import vector_add

begin_time = datetime.datetime.now()

NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
LEFT, RIGHT = 0, 1
moves = { NORTH: (0, -1), SOUTH: (0, 1), EAST: (+1, 0), WEST: (-1, 0) }
turns = { LEFT:     (WEST, NORTH, EAST, SOUTH),
          RIGHT:    (EAST, SOUTH, WEST, NORTH),}

cur_dir = NORTH
weakened = set()
infected = set()
flagged = set()

cur_pos = tuple([0, 0])

with open('./input.txt') as f:
    grid = []
    while line := f.readline().rstrip():
        grid.append(line[:])

    offset = len(grid) // 2
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == '#':
                infected.add((x - offset, y - offset))

infections = 0
for burst in range(10000000):
    if cur_pos in flagged:
        cur_dir = turns[LEFT][turns[LEFT][cur_dir]]
        flagged.remove(cur_pos)

    elif cur_pos in weakened:
        infections += 1

        infected.add(cur_pos)
        weakened.remove(cur_pos)

    elif cur_pos in infected:
        cur_dir = turns[RIGHT][cur_dir]

        flagged.add(cur_pos)
        infected.remove(cur_pos)

    else:
        cur_dir = turns[LEFT][cur_dir]
        weakened.add(cur_pos)

    cur_pos = tuple(vector_add(cur_pos, moves[cur_dir]))

print(infections)
print(datetime.datetime.now() - begin_time)
