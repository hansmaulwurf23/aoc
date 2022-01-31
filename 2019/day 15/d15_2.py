import datetime
from collections import deque

import showgrid
from aopython import min_max_2d, vector_add
from intcode import IntCodeMachine

begin_time = datetime.datetime.now()

WALL, NIL, OXY = 0, 1, 2
NORTH, SOUTH, WEST, EAST = 1, 2, 3, 4
clockwise = (None, EAST, WEST, NORTH, SOUTH)
cclockwise = (None, WEST, EAST, SOUTH, NORTH)
moves = { NORTH: (0, 1), SOUTH: (0, -1), EAST: (+1, 0), WEST: (-1, 0) }


def adjacents(pos, maze):
    for m in moves.values():
        a = tuple(vector_add(pos, m))
        if a in maze:
            yield a


# https://en.wikipedia.org/wiki/Breadth-first_search
def bfs_longest(root, maze):
    q = deque()
    visited = set()
    visited.add(root)
    q.appendleft((root, 0))
    while q:
        node, steps = q.pop()
        for a in adjacents(node, maze):
            if a not in visited:
                visited.add(a)
                q.appendleft((a, steps + 1))

        if not q:
            return steps



# http://www.astrolog.org/labyrnth/algrithm.htm#solve
# wall follower
def explore(vm, startdir, startpos):
    position, direction = startpos, startdir
    maze = set()
    oxygen_position = None

    while True:
        # since we can only reside in a path of this maze turn and check if we
        # move along the walls
        test_direction = cclockwise[direction]
        cell = vm.run_to_output([test_direction])

        if cell == WALL:
            # nice, turning means hitting the wall, what if we keep going our direction
            cell = vm.run_to_output([direction])

            if cell == WALL:
                # still a wall, we seem at a turn -> turn and loop
                direction = clockwise[direction]
            else:
                position = tuple(vector_add(position, moves[direction]))
                if cell == OXY:
                    oxygen_position = position
                maze.add(position)
        else:
            position = tuple(vector_add(position, moves[test_direction]))
            if cell == OXY:
                oxygen_position = position
            maze.add(position)
            direction = test_direction

        if position == startpos:
            # print(f'back at origin with direction {direction}')
            if direction == startdir:
                break

    return maze, oxygen_position


with open('./input.txt') as f:
    program = [int(x) for x in f.readlines()[0].split(',')]

vm = IntCodeMachine(program)
maze, oxy = explore(vm, NORTH, (0, 0))
showgrid.show_grid(list(maze), highlights=[(0, 0), oxy])
print(oxy)
steps = bfs_longest(oxy, maze)
print(steps)

print(datetime.datetime.now() - begin_time)
