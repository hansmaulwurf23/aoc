import datetime
begin_time = datetime.datetime.now()

NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
turns = {'L': (WEST, NORTH, EAST, SOUTH),
         'R': (EAST, SOUTH, WEST, NORTH)}
moves = { NORTH: (0, 1), SOUTH: (0, -1), EAST: (+1, 0), WEST: (-1, 0) }


with open('./input.txt') as f:
    cmds = f.readlines()[0].split(', ')

cur_dir = NORTH
cur_pos = (0, 0)
for m in cmds:
    turn = m[0]
    cur_dir = turns[turn][cur_dir]
    length = int(m[1:])
    mx, my = moves[cur_dir]
    cur_pos = (cur_pos[0] + mx * length, cur_pos[1] + my * length)

print(abs(cur_pos[0]) + abs(cur_pos[1]))
print(datetime.datetime.now() - begin_time)
