import datetime

from intcode import IntCodeMachine

begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    program = [int(x) for x in f.readlines()[0].split(',')]

vm = IntCodeMachine(program)
print(vm.run([5])[-1])
print(datetime.datetime.now() - begin_time)
