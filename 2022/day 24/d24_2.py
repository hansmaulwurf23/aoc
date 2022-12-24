import datetime
from collections import defaultdict, Counter

from aopython import vector_add

begin_time = datetime.datetime.now()
N, E, S, W = range(4)
MOVES = {N: (0, -1), E: (1, 0), S: (0, 1), W: (-1, 0)}
SYM = {N: '^', S: 'v', E: '>', W: '<'}
DIR = {v: k for k, v in SYM.items()}

cur_pos, finish, start = None, None, None
map_width, map_height = None, None
storms = defaultdict(list)
PROD = True
file, printing = {True:  ('./input.txt',   False),
                  False: ('./example.txt', True)}[PROD]


def print_field():
    global storms, finish, start, map_height, map_width
    for y in range(-1, map_height.stop + 1):
        for x in range(-1, map_width.stop + 1):
            p = (x, y)
            if is_in_map(p):
                if p in storms:
                    print(SYM[storms[p][0]] if len(storms[p]) == 1 else len(storms[p]), end='')
                else:
                    print('.', end='')
            else:
                if p in (start, finish):
                    print('.', end='')
                else:
                    print('#', end='')
        print('')


def update_storms():
    global storms
    new_storms = defaultdict(list)
    for pos, directions in storms.items():
        for direction in directions:
            new_pos = tuple(vector_add(pos, MOVES[direction]))
            if not is_in_map(new_pos):
                if direction == N:
                    new_pos = (new_pos[0], map_height.stop - 1)
                elif direction == S:
                    new_pos = (new_pos[0], 0)
                elif direction == E:
                    new_pos = (0, new_pos[1])
                elif direction == W:
                    new_pos = (map_width.stop - 1, new_pos[1])

            new_storms[new_pos].append(direction)

    storms.clear()
    storms |= new_storms


def is_in_map(p):
    global map_width, map_height
    x, y = p
    return x in map_width and y in map_height


def bfs(start, finish):
    global printing, storms

    minute = 0
    at_finish = False
    states = {start}
    while not at_finish:
        next_states = set()
        update_storms()
        for state_pos in states:
            for next_pos in [tuple(vector_add(state_pos, d)) for d in MOVES.values()] + [state_pos]:
                if next_pos == finish:
                    at_finish = True
                    break
                if (is_in_map(next_pos) or next_pos == start) and next_pos not in storms:
                    next_states.add(next_pos)
        states = next_states

        minute += 1
    return minute


with open(file) as f:
    lines = f.readlines()
    start = (lines[0].index('.') - 1, -1)
    finish = (lines[-1].index('.') - 1, len(lines) - 2)
    for y, line in enumerate(lines[1:-1]):
        for x, c in enumerate(line.rstrip()[1:-1]):
            if c in SYM.values():
                storms[(x, y)].append(DIR[c])
    map_width = range(0, len(line) - 3)
    map_height = range(0, len(lines) - 2)

all_minutes = 0
all_minutes += bfs(start, finish)
all_minutes += bfs(finish, start)
all_minutes += bfs(start, finish)

print(all_minutes)
print(datetime.datetime.now() - begin_time)
