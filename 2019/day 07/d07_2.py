import datetime
from itertools import permutations

from intcode import IntCodeMachine

begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    program = [int(x) for x in f.readlines()[0].split(',')]


def run_prog(prog, inputs, pc):
    while prog[pc] != 99:
        raw = prog[pc]
        opcode = raw % 10
        param_mode1 = (raw // 100) % 10
        param_mode2 = (raw // 1000) % 10

        # add
        if opcode == 1:
            op1 = prog[pc + 1] if param_mode1 == 1 else prog[prog[pc + 1]]
            op2 = prog[pc + 2] if param_mode2 == 1 else prog[prog[pc + 2]]
            prog[prog[pc + 3]] = op1 + op2
            pc += 4
        # mul
        elif opcode == 2:
            op1 = prog[pc + 1] if param_mode1 == 1 else prog[prog[pc + 1]]
            op2 = prog[pc + 2] if param_mode2 == 1 else prog[prog[pc + 2]]
            prog[prog[pc + 3]] = op1 * op2
            pc += 4
        # read
        elif opcode == 3:
            op1 = prog[pc + 1]
            prog[op1] = inputs.pop(0)
            pc += 2
        # write
        elif opcode == 4:
            op1 = prog[pc + 1] if param_mode1 == 1 else prog[prog[pc + 1]]
            cur_out = op1
            pc += 2
            return cur_out, pc
        # jump-if-true
        elif opcode == 5:
            op1 = prog[pc + 1] if param_mode1 == 1 else prog[prog[pc + 1]]
            op2 = prog[pc + 2] if param_mode2 == 1 else prog[prog[pc + 2]]
            pc = op2 if op1 != 0 else pc + 3
        # jump-if-false
        elif opcode == 6:
            op1 = prog[pc + 1] if param_mode1 == 1 else prog[prog[pc + 1]]
            op2 = prog[pc + 2] if param_mode2 == 1 else prog[prog[pc + 2]]
            pc = op2 if op1 == 0 else pc + 3
        # less than
        elif opcode == 7:
            op1 = prog[pc + 1] if param_mode1 == 1 else prog[prog[pc + 1]]
            op2 = prog[pc + 2] if param_mode2 == 1 else prog[prog[pc + 2]]
            prog[prog[pc + 3]] = 1 if op1 < op2 else 0
            pc += 4
        # equals
        elif opcode == 8:
            op1 = prog[pc + 1] if param_mode1 == 1 else prog[prog[pc + 1]]
            op2 = prog[pc + 2] if param_mode2 == 1 else prog[prog[pc + 2]]
            prog[prog[pc + 3]] = 1 if op1 == op2 else 0
            pc += 4
        else:
            print(f'unknown op code! {opcode}')
            break

    # None means halted on 99
    return None, pc


def run_configuration(program, phase_sequence, input_signal):
    last_out = input_signal
    vms = [IntCodeMachine(program) for _ in range(5)]

    for i in range(5):
        last_out = vms[i].run_to_output([phase_sequence.pop(0), last_out])

    all_running = True
    while all_running:
        for i in range(5):
            last_out = vms[i].run_to_output([last_out])

            if vms[i].terminated:
                all_running = False
            elif i == 4:
                amp_e_out = last_out

    return amp_e_out


res = dict()
for p in permutations([5, 6, 7, 8, 9]):
    res[p] = run_configuration(program, list(p), 0)
    # print(p, res[p])

print(max(res.values()))
print(datetime.datetime.now() - begin_time)
