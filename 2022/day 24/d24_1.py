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
                  False: ('./example.txt', False)}[PROD]


def print_field():
    global storms, finish, start, map_height, map_width
    for y in range(map_height.stop + 1):
        for x in range(map_width.stop + 1):
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
                    new_pos = (new_pos[0], 1)
                elif direction == E:
                    new_pos = (1, new_pos[1])
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
    # states = {(cur_pos, (cur_pos,))}
    states = {start}
    if printing: print_field()
    while not at_finish:
        update_storms()
        next_states = set()
        print(f'minute {minute} states {len(states)}')
        # for state_pos, path in states:
        for state_pos in states:
            for next_pos in [tuple(vector_add(state_pos, d)) for d in MOVES.values()] + [state_pos]:
                if next_pos == finish:
                    # print(minute + 1, path)
                    at_finish = True
                    break
                if next_pos not in storms and (is_in_map(next_pos) or next_pos == start):
                    # next_states.add((next_pos, tuple(path + (next_pos,))))
                    next_states.add(next_pos)
        states = next_states
        if printing: print_field()
        minute += 1
    return minute


with open(file) as f:
    lines = f.readlines()
    start = (lines[0].index('.'), 0)
    finish = (lines[-1].index('.'), len(lines) - 1)
    for y, line in enumerate(lines):
        for x, c in enumerate(line.rstrip()):
            if c in SYM.values():
                storms[(x, y)].append(DIR[c])
    map_width = range(1, len(line) - 1)
    map_height = range(1, len(lines) - 1)


if dict(Counter([v[0] for k, v in storms.items()])) != {1: 801, 2: 800, 3: 798, 0: 744}:
    print('Direction counter wrong! Example?')

print(bfs(start, finish))


print(datetime.datetime.now() - begin_time)
