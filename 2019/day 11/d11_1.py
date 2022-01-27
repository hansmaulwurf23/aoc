import datetime
from intcode import IntCodeMachine
from aopython import vector_add
from collections import defaultdict

begin_time = datetime.datetime.now()

# ordered so that turn +1 / -1 updates directions accordingly
#               UP     RIGHT    DOWN    LEFT
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
turns = {0: -1, 1: 1}

with open('./input.txt') as f:
    program = [int(x) for x in f.readlines()[0].split(',')]

vm = IntCodeMachine(program)
direction = 0
position = (0, 0)
panels = defaultdict(lambda : 0)
while not vm.terminated:
    color = vm.run_to_output([panels[position]])
    turn = vm.run_to_output([panels[position]])
    if turn is not None and vm.terminated == False:
        panels[position] = color
        direction = (direction + turns[turn] + 4) % 4
        position = tuple(vector_add(position, directions[direction]))

print(len(panels))
print(datetime.datetime.now() - begin_time)
