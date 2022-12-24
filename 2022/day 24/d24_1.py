import datetime
from collections import defaultdict

from aopython import vector_add

begin_time = datetime.datetime.now()
N, E, S, W = range(4)
MOVES = {N: (0, -1), E: (1, 0), S: (0, 1), W: (-1, 0)}
SYM = {N: '^', S: 'v', E: '>', W: '<'}
DIR = {v: k for k, v in SYM.items()}

cur_pos, finish, start = None, None, None
map_width, map_height = None, None
storms = defaultdict(list)


def update_storms(old_storms):
    new_storms = defaultdict(list)
    for pos, directions in old_storms.items():
        for direction in directions:
            new_pos = tuple(vector_add(pos, MOVES[direction]))
            if not is_in_map(new_pos):
                if direction == N:
                    new_pos = (new_pos[0], map_height.stop - 1)
                elif direction == S:
                    new_pos = (new_pos[0], 1)
                elif direction == E:
                    new_pos = (1, new_pos[1])
                elif direction == W:
                    new_pos = (map_width.stop - 1, new_pos[1])

            new_storms[new_pos].append(direction)

    return new_storms


def is_in_map(p):
    global map_width, map_height
    x, y = p
    return x in map_width and y in map_height


with open('./input.txt') as f:
    lines = f.readlines()
    start = (lines[0].index('.'), 0)
    finish = (lines[-1].index('.'), len(lines) - 1)
    for y, line in enumerate(lines):
        for x, c in enumerate(line.rstrip()):
            if c in SYM.values():
                storms[(x, y)].append(DIR[c])
    map_width = range(1, len(line) - 1)
    map_height = range(1, len(lines) - 1)


minute = 0
cur_pos = tuple(start)
states = {(cur_pos, (cur_pos,))}
while True:
    storms = update_storms(storms)
    next_states = set()
    print(f'minute {minute} states {len(states)}')
    for state_pos, path in states:
        for next_pos in [tuple(vector_add(state_pos, d)) for d in MOVES.values()] + [state_pos]:
            if next_pos == finish:
                print(minute + 1, path)
                exit(0)
            if next_pos not in storms and (is_in_map(next_pos) or next_pos == start):
                next_states.add((next_pos, tuple(path + (next_pos,))))
    states = next_states
    minute += 1


print(datetime.datetime.now() - begin_time)
