import datetime
begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    numbers = [int(x) for x in f.readlines()[0].split(',')]


def run_prog(numbers, cur_in):
    pc = 0
    cur_out = None
    while numbers[pc] != 99:
        print(pc)
        raw = numbers[pc]
        opcode = raw % 10
        param_mode1 = (raw // 100) % 10
        param_mode2 = (raw // 1000) % 10

        # add
        if opcode == 1:
            op1 = numbers[pc + 1] if param_mode1 == 1 else numbers[numbers[pc + 1]]
            op2 = numbers[pc + 2] if param_mode2 == 1 else numbers[numbers[pc + 2]]
            numbers[numbers[pc + 3]] = op1 + op2
            pc += 4
        # mul
        elif opcode == 2:
            op1 = numbers[pc + 1] if param_mode1 == 1 else numbers[numbers[pc + 1]]
            op2 = numbers[pc + 2] if param_mode2 == 1 else numbers[numbers[pc + 2]]
            numbers[numbers[pc + 3]] = op1 * op2
            pc += 4
        # read
        elif opcode == 3:
            op1 = numbers[pc + 1]
            numbers[op1] = cur_in
            pc += 2
        # write
        elif opcode == 4:
            op1 = numbers[pc + 1] if param_mode1 == 1 else numbers[numbers[pc + 1]]
            cur_out = op1
            pc += 2
        # jump-if-true
        elif opcode == 5:
            op1 = numbers[pc + 1] if param_mode1 == 1 else numbers[numbers[pc + 1]]
            op2 = numbers[pc + 2] if param_mode2 == 1 else numbers[numbers[pc + 2]]
            pc = op2 if op1 != 0 else pc + 3
        # jump-if-false
        elif opcode == 6:
            op1 = numbers[pc + 1] if param_mode1 == 1 else numbers[numbers[pc + 1]]
            op2 = numbers[pc + 2] if param_mode2 == 1 else numbers[numbers[pc + 2]]
            pc = op2 if op1 == 0 else pc + 3
        # less than
        elif opcode == 7:
            op1 = numbers[pc + 1] if param_mode1 == 1 else numbers[numbers[pc + 1]]
            op2 = numbers[pc + 2] if param_mode2 == 1 else numbers[numbers[pc + 2]]
            numbers[numbers[pc + 3]] = 1 if op1 < op2 else 0
            pc += 4
        # equals
        elif opcode == 8:
            op1 = numbers[pc + 1] if param_mode1 == 1 else numbers[numbers[pc + 1]]
            op2 = numbers[pc + 2] if param_mode2 == 1 else numbers[numbers[pc + 2]]
            numbers[numbers[pc + 3]] = 1 if op1 == op2 else 0
            pc += 4
        else:
            print(f'unknown op code! {opcode}')
            break

    return cur_out


print(run_prog(numbers, 5))
print(datetime.datetime.now() - begin_time)
