import datetime

from aopython import vector_add

begin_time = datetime.datetime.now()
NORTH, EAST, SOUTH, WEST = '^', '>', 'v', '<'
MOVES = { NORTH: (0, 1), SOUTH: (0, -1), EAST: (+1, 0), WEST: (-1, 0) }

pos = (0, 0)
seen = {pos}
for m in open('./input.txt').readline().rstrip():
    pos = tuple(vector_add(pos, MOVES[m]))
    seen.add(pos)

print(len(seen))
print(datetime.datetime.now() - begin_time)
