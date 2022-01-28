import datetime
from intcode import IntCodeMachine

begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    program = [int(x) for x in f.readlines()[0].split(',')]

vm = IntCodeMachine(program)
outputs = vm.run(program)
blocks = set()
for i in range(0, len(outputs), 3):
    x, y, t = outputs[i:i+3]
    if t == 2:
        blocks.add((x, y))
print(len(blocks))
print(datetime.datetime.now() - begin_time)
