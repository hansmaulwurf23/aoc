import datetime
from itertools import permutations

from intcode import IntCodeMachine

begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    program = [int(x) for x in f.readlines()[0].split(',')]


def run_configuration(program, phase_sequence, input_signal):
    last_out = input_signal
    for i in range(5):
        vm = IntCodeMachine(program)
        last_out = vm.run([phase_sequence.pop(0), last_out])[-1]
    return last_out


res = dict()
for p in permutations([0, 1, 2, 3, 4]):
    res[p] = run_configuration(program, list(p), 0)
    # print(p, res[p])

print(max(res.values()))
print(datetime.datetime.now() - begin_time)
