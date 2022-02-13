import datetime
from iointcode import IOIntCodeMachine, BroadcastException

begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    program = [int(x) for x in f.readlines()[0].split(',')]

network = []
for addr in range(50):
    network.append(IOIntCodeMachine(program, network, [addr]))

while True:
    try:
        for i, vm in enumerate(network):
            print(i, vm.in_queue, vm.outputs)
            vm.run_to_input([])
    except BroadcastException as e:
        print(f'{e.vals}')
        break

print(datetime.datetime.now() - begin_time)
