import datetime

import showgrid
from aopython import vector_add

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
tower = set()


def has_collision(rock, block_pos, direction):
    new_pos = tuple(vector_add(block_pos, direction))
    rock_elems = list(map(lambda e: tuple(vector_add(e, new_pos)), ROCK[rock]))
    if direction != DOWN and not all(map(lambda e: 0 <= e[0] < 7, rock_elems)):
        # print('collision on left or right wall')
        return True

    if direction == DOWN and not all(map(lambda e: e[1] >= 0, rock_elems)):
        # print('collision on ground')
        return True

    if not all(map(lambda e: e not in tower, rock_elems)):
        # print('collision with another rock')
        return True

    return False


def fall_into_place(rock, top):
    global tower, cur_gas_mvmt
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
                tower |= set(map(lambda e: tuple(vector_add(e, block_pos)), ROCK[rock]))
                return
        else:
            block_pos = tuple(vector_add(block_pos, delta))

        move = move + 1
        direction = move % 2


with open('./input.txt') as f:
    gas_mvmt.extend(map(lambda x: LEFT if x == '<' else RIGHT, f.readline().rstrip()))

for r in range(2022):
    top = max(map(lambda r: r[1], tower)) + 1 if tower else 0
    # print(f'new height {top}')
    fall_into_place(ROCK_TYPES[r % len(ROCK_TYPES)], top)
    # showgrid.show_grid(tower)

top = max(map(lambda r: r[1], tower)) + 1 if tower else 0
print(f'height {top}')
print('       3141')
print(datetime.datetime.now() - begin_time)
