import datetime
import showgrid
from aopython import min_max_2d, vector_add
from intcode import IntCodeMachine

begin_time = datetime.datetime.now()

NORTH, SOUTH, WEST, EAST = map(ord, ['^', 'v', '<', '>'])
moves = { NORTH: (0, 1), SOUTH: (0, -1), EAST: (+1, 0), WEST: (-1, 0) }
SCAFFOLD = 35


def adjacents(pos):
    for m in moves.values():
        yield tuple(vector_add(pos, m))


def get_scaffold(output):
    scaffolds = set()
    x, y = 0, 0
    for o in output:
        if o == 10:
            x = 0
            y += 1
        else:
            if o == 35:
                scaffolds.add((x, y))
            elif o in moves.keys():
                scaffolds.add((x, y))
                robot = (x, y)
            x += 1

    return scaffolds, robot


def get_intersections(scaffolds):
    intersections = set()
    for s in scaffolds:
        if len(list(filter(lambda x: x in scaffolds, adjacents(s)))) == 4:
            intersections.add(s)
    return intersections


with open('./input.txt') as f:
    program = [int(x) for x in f.readlines()[0].split(',')]

vm = IntCodeMachine(program)
output = vm.run([])
scaffolds, robot = get_scaffold(output)
intersections = get_intersections(scaffolds)

print(sum(map(lambda x: x[0] * x[1], intersections)))
showgrid.show_grid(scaffolds, highlights=intersections)
print(datetime.datetime.now() - begin_time)
