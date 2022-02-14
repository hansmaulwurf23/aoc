import datetime
from iointcode import IOIntCodeMachine, BroadcastException

begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    program = [int(x) for x in f.readlines()[0].split(',')]

network = []
for addr in range(50):
    network.append(IOIntCodeMachine(program, network, [addr]))

last_broadcast = None
last_wakeup_broadcast = None
while True:
    try:
        for i, vm in enumerate(network):
            # print(i, vm.in_queue, vm.outputs, vm.idle)
            vm.run_to_input([])

            if all(vm.idle for vm in network):
                # print(f'IDLE. Waking up hero zero with {last_broadcast}. current queue of zero {network[0].in_queue}')
                network[0].idle = False
                network[0].in_queue.extend(last_broadcast)
                if last_wakeup_broadcast is not None and last_broadcast[1] == last_wakeup_broadcast[1]:
                    print(last_wakeup_broadcast[1])
                    print(datetime.datetime.now() - begin_time)
                    exit(0)
                else:
                    last_wakeup_broadcast = last_broadcast

    except BroadcastException as e:
        last_broadcast = e.vals
