import datetime
from itertools import permutations
begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    programm = [int(x) for x in f.readlines()[0].split(',')]


def run_prog(prog, inputs):
    pc = 0
    cur_out = None
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
            if len(inputs) > 1:
                prog[op1] = inputs.pop(0)
            else:
                prog[op1] = inputs[0]
            pc += 2
        # write
        elif opcode == 4:
            op1 = prog[pc + 1] if param_mode1 == 1 else prog[prog[pc + 1]]
            cur_out = op1
            pc += 2
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

    return cur_out


def run_configuration(programm, phase_sequence, input_signal):
    last_out = input_signal
    for i in range(5):
        last_out = run_prog(programm.copy(), [phase_sequence.pop(0), last_out])
    return last_out


res = dict()
for p in permutations([0,1,2,3,4]):
    res[p] = run_configuration(programm, list(p), 0)
    # print(p, res[p])

print(max(res.values()))
print(datetime.datetime.now() - begin_time)
