import datetime

import showgrid
from aopython import vector_add, bool_list_to_int

begin_time = datetime.datetime.now()

LEFT, RIGHT, DOWN = (-1, 0), (1, 0), (0, -1)
GAS, GRAVITY = range(2)
ROCK_TYPES = ['-', '+', 'L', '|', 'o']
# rocks relative to bottom left corner
ROCK = {
    '-': [(0, 0), (1, 0), (2, 0), (3, 0)],
    '+': [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    'L': [(2, 2), (2, 1), (0, 0), (1, 0), (2, 0)],
    '|': [(0, 0), (0, 1), (0, 2), (0, 3)],
    'o': [(0, 0), (1, 0), (0, 1), (1, 1)]
}

gas_mvmt = []
cur_gas_mvmt = 0
stack_height = 0
tower = []


def has_collision(rock, block_pos, direction):
    new_pos = tuple(vector_add(block_pos, direction))
    rock_elems = list(map(lambda e: tuple(vector_add(e, new_pos)), ROCK[rock]))
    if not all(map(lambda e: 0 <= e[0] < 7, rock_elems)):
        # print('collision on left or right wall')
        return True

    if direction == DOWN and not all(map(lambda e: e[1] >= 0, rock_elems)):
        # print('collision on ground')
        return True

    if any(map(lambda e: len(tower) > e[1] and tower[e[1]][e[0]], rock_elems)):
        # print('collision with another rock')
        return True

    return False


def fall_into_place(r):
    global tower, cur_gas_mvmt
    top = len(tower) if tower else 0
    rock = ROCK_TYPES[r % len(ROCK_TYPES)]
    block_pos = (2, top + 3)

    move, direction = 0, 0
    while True:
        if direction == GAS:
            delta = gas_mvmt[cur_gas_mvmt]
            cur_gas_mvmt = (cur_gas_mvmt + 1) % len(gas_mvmt)
            # print(f'move {"right" if delta == RIGHT else "left"}')
        elif direction == GRAVITY:
            delta = DOWN
            # print('move down')

        if has_collision(rock, block_pos, delta):
            if direction == GAS:
                # keep on falling in a free world
                pass
            else:
                # collision with rock, stop falling and rest
                new_lines = 0
                for ex, ey in map(lambda e: tuple(vector_add(e, block_pos)), ROCK[rock]):
                    while len(tower) <= ey:
                        new_lines += 1
                        tower.append([False] * 7)
                    tower[ey][ex] = True
                return new_lines
        else:
            block_pos = tuple(vector_add(block_pos, delta))

        move = move + 1
        direction = move % 2


with open('./input.txt') as f:
    gas_mvmt.extend(map(lambda x: LEFT if x == '<' else RIGHT, f.readline().rstrip()))

runs = 1000000000000
detection_range = 4  # started this with 12 lines converted to ints lol
seen = {}
period, periodic_growth = None, None

for r in range(runs):
    rock_type = r % len(ROCK_TYPES)
    fall_into_place(r)

    pattern = [rock_type, cur_gas_mvmt]
    for line in tower[-detection_range:]:
        pattern.append(bool_list_to_int(line))
    pattern = tuple(pattern)
    if pattern in seen:
        seen_r, seen_height = seen[pattern]
        period = r - seen_r
        periodic_growth = len(tower) - seen_height
        break
    else:
        seen[pattern] = (r, len(tower))

height = len(tower)
num_repeats = (runs - r) // period
r += period * num_repeats + 1
height += periodic_growth * num_repeats

while r < runs:
    height += fall_into_place(r)
    r += 1

print(f'{height}')
print(1561739130391)
print(datetime.datetime.now() - begin_time)
