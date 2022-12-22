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

def print_grid(path):
    walls = set()
    for y in range(len(map)):
        for x, c in enumerate(map[y]):
            if c == '#':
                walls.add((x, y))

    showgrid.show_grid(walls, highlights=path, invert_yaxis=True, s=4, highlightsize=4)

def next_pos(cur_pos, cur_dir):
    new_pos = vector_add(cur_pos, MOVES[cur_dir])
    x, y = new_pos
    if y >= len(map) or (cur_dir == DOWN and map[y][x] == ' '):
        # bottom out
        for y in range(len(map)):
            if map[y][x] != ' ':
                return x, y
    if y < 0 or (cur_dir == UP and map[y][x] == ' '):
        # upper bound
        for y in range(len(map) - 1, -1, -1):
            if map[y][x] != ' ':
                return x, y
    if x >= len(map[y]) or (cur_dir == RIGHT and map[y][x] == ' '):
        # right out
        for x in range(len(map[y])):
            if map[y][x] != ' ':
                return x, y
    if x < 0 or (cur_dir == LEFT and map[y][x] == ' '):
        # left out
        for x in range(len(map[y]) - 1, -1, -1):
            if map[y][x] != ' ':
                return x, y

    # i'll have none of that
    return new_pos


with open('./input.txt') as f:
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
            new_pos = next_pos(cur_pos, cur_dir)
            target = map[new_pos[1]][new_pos[0]]
            if target == '.':
                cur_pos = tuple(new_pos)
                path.add(cur_pos)
            if target == '#':
                break
    else:
        cur_dir = TURNR[cur_dir] if c == 'R' else TURNL[cur_dir]

# print_grid(path)
print(cur_pos, cur_dir)
print(sum([(cur_pos[0] + 1) * 4, (cur_pos[1] + 1) * 1000, cur_dir]))
print(datetime.datetime.now() - begin_time)
