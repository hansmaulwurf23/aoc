import datetime

import showgrid
from intcode import IntCodeMachine

begin_time = datetime.datetime.now()

NIL = 0
BEAM = 1

with open('./input.txt') as f:
    program = [int(x) for x in f.readlines()[0].split(',')]

vm = IntCodeMachine(program)

def eval_drone(x, y):
    vm.reset(program.copy())
    return vm.run_to_output([x, y])


beams = set()
lower_y = 0
x = 50
upper_y = x
square_size = 100
coords_diff = square_size - 1
while eval_drone(x, upper_y) == NIL:
    vm.reset(program.copy())
    upper_y -= 1

while True:
    while eval_drone(x, upper_y) == BEAM:
        upper_y += 1
    upper_y -= 1

    # find lower bound 100 x's further down the road, since the width of the ship must fit in there
    while eval_drone(x + coords_diff, lower_y) == NIL:
        lower_y += 1

    if upper_y - lower_y >= coords_diff:
        break

    x += 1

print(x * 10000 + lower_y)
print('10180726')
print(datetime.datetime.now() - begin_time)
