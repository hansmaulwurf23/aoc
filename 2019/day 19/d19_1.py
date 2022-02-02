import datetime

import showgrid
from intcode import IntCodeMachine

begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    program = [int(x) for x in f.readlines()[0].split(',')]

beams = set()
for x, y in [(x, y) for x in range(50) for y in range(50)]:
    vm = IntCodeMachine(program.copy())
    if vm.run_to_output([x, y]) > 0:
        beams.add((x, y))

showgrid.show_grid(beams)
print(len(beams))
print(datetime.datetime.now() - begin_time)
