import datetime
import re
import showgrid
from aopython import vector_add

begin_time = datetime.datetime.now()

RIGHT, DOWN, LEFT, UP = range(4)
TURNR = (DOWN, LEFT, UP, RIGHT)
TURNL = (UP, RIGHT, DOWN, LEFT)
MOVES = {RIGHT: (1, 0), DOWN: (0, 1), UP: (0, -1), LEFT: (-1, 0)}

map = []
cmds = []
# for faces see notes as well!
faces = {(1, 0): 1, (2, 0): 2, (1, 1): 3, (0, 2): 4, (1, 2): 5, (0, 3): 6}
face_len, file = 50, './input.txt'
# face_len, file = 4, './example.txt'

def print_grid(path):
    walls = set()
    for y in range(len(map)):
        for x, c in enumerate(map[y]):
            if c == '#':
                walls.add((x, y))

    showgrid.show_grid(walls, highlights=path, invert_yaxis=True, s=4, highlightsize=4)

def next_pos(cur_pos, cur_dir):
    face = faces[(cur_pos[0] // face_len, cur_pos[1] // face_len)]
    new_pos = vector_add(cur_pos, MOVES[cur_dir])
    x, y = new_pos
    fx, fy = cur_pos[0] % face_len, cur_pos[1] % face_len

    if y < 0:
        if face == 1:
            return (0, 3 * face_len + fx), RIGHT    # OK
        elif face == 2:
            return (fx, 4 * face_len - 1), UP       # OK
        raise "top out wrong"
    if y >= len(map):
        if face == 6:
            return (fx, 0), DOWN                    # OK
        raise "bottom out wrong"
    if x >= len(map[0]):
        if face == 2:
            return (2 * face_len - 1, 2 * face_len + face_len - fy - 1), LEFT  # OK
        raise "right out wrong"
    if x < 0:
        if face == 4:
            return (face_len, face_len - fy - 1), RIGHT    # OK
        elif face == 6:
            return (face_len + fy, 0), DOWN         # OK
        raise "left out wrong"

    target = map[y][x]
    if target == ' ':
        if cur_dir == LEFT:
            if face == 1:
                return (0, 2 * face_len + (face_len - fy) - 1), RIGHT
            if face == 3:
                return (fy, 2 * face_len), DOWN
        if cur_dir == RIGHT:
            if face == 3:
                return (2 * face_len + fy, face_len - 1), UP
            if face == 5:
                return (3 * face_len - 1, face_len - fy), LEFT
            if face == 6:
                return (face_len + fy, 3 * face_len - 1), UP
        if cur_dir == DOWN:
            if face == 2:
                return (2 * face_len - 1, face_len + fx), LEFT
            if face == 5:
                return (face_len - 1, 3 * face_len + fx), LEFT
        if cur_dir == UP:
            if face == 4:
                return (face_len, face_len + fx), RIGHT

    # i'll have none of that
    return new_pos, cur_dir


with open(file) as f:
    lines = f.readlines()
    ll = len(lines[0].rstrip())
    for line in [l.rstrip() for l in lines[:-2]]:
        map.append(tuple(line.ljust(ll, ' ')))

    line = lines[-1].rstrip()
    lenghts = re.split('L|R', line)
    turns = re.split('\d+', line)[1:]
    for l, t in zip(lenghts, turns):
        cmds.append(int(l))
        if t:
            cmds.append(t)

cur_pos = (map[0].index('.'), 0)
cur_dir = RIGHT
path = set([cur_pos])
for c in cmds:
    if isinstance(c, int):
        for s in range(c):
            new_pos, cur_dir = next_pos(cur_pos, cur_dir)
            target = map[new_pos[1]][new_pos[0]]
            if target == '.':
                cur_pos = tuple(new_pos)
                path.add(cur_pos)
            if target == '#':
                break
    else:
        cur_dir = TURNR[cur_dir] if c == 'R' else TURNL[cur_dir]

print_grid(path)
print(cur_pos, cur_dir)
print(sum([(cur_pos[0] + 1) * 4, (cur_pos[1] + 1) * 1000, cur_dir]))
print(datetime.datetime.now() - begin_time)
