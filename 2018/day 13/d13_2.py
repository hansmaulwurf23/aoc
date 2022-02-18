import datetime
from collections import defaultdict

from aopython import vector_add

begin_time = datetime.datetime.now()

NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
dir_symbols = ('^', '>', 'v', '<')
LEFT, RIGHT, STRAIGHT = 0, 1, 2
turns = { LEFT:     (WEST, NORTH, EAST, SOUTH),
          RIGHT:    (EAST, SOUTH, WEST, NORTH),
          STRAIGHT: (NORTH, EAST, SOUTH, WEST)}
inv_dir = (SOUTH, WEST, NORTH, EAST)
turn_cycle = (STRAIGHT, LEFT, RIGHT)
moves = { NORTH: (0, -1), SOUTH: (0, 1), EAST: (+1, 0), WEST: (-1, 0) }

# key = (x, y) value = (adjacent directions)
tracks = defaultdict(tuple)
# key = (x, y) value = (cur_dir, next_intersection_turn)
carts = dict()


def is_intersection(pos):
    return len(tracks[pos]) == 4


def tick(carts):
    new_carts = dict()
    # iterate over carts sorted by y and then x
    for y, x in sorted(list(map(lambda p: (p[1], p[0]), carts.keys()))):
        cur_pos = (x, y)
        if cur_pos not in carts:
            # cart collided this tick
            continue
        cur_dir, next_turn = carts[cur_pos]
        if is_intersection(cur_pos):
            next_dir = turns[next_turn][cur_dir]
            next_turn = turn_cycle[next_turn]
        else:
            next_dir = next((d for d in tracks[cur_pos] if d != inv_dir[cur_dir]))

        next_pos = tuple(vector_add(cur_pos, moves[next_dir]))

        if next_pos in new_carts:
            del new_carts[next_pos]
            print(f'COLLIDE(n)! {next_pos} {len(carts) + len(new_carts)}')
        elif next_pos in carts:
            del carts[next_pos]
            print(f'COLLIDE(o)! {next_pos} {len(carts) + len(new_carts)}')
        else:
            new_carts[next_pos] = (next_dir, next_turn)
            del carts[cur_pos]

    if len(new_carts) <= 1:
        print(f'lonely cart left: {new_carts}')
        return None
    return new_carts


with open('./input.txt') as f:
    y = 0
    while line := f.readline().rstrip():
        for x, c in enumerate(line):
            if (dir := dir_symbols.index(c) if c in dir_symbols else None) is not None:
                carts[(x, y)] = (dir, LEFT)

            if c == '-' or dir in (EAST, WEST):
                tracks[(x, y)] = (EAST, WEST)
            elif c == '|' or dir in (NORTH, SOUTH):
                tracks[(x, y)] = (NORTH, SOUTH)
            elif c in ('/', '\\'):
                tracks[(x, y)] = (WEST if EAST in tracks[(x - 1, y)] else EAST,
                                  NORTH if SOUTH in tracks[(x, y - 1)] else SOUTH)
            elif c == '+':
                tracks[(x, y)] = (NORTH, EAST, SOUTH, WEST)

        y += 1

while carts is not None:
    carts = tick(carts)
print(datetime.datetime.now() - begin_time)
