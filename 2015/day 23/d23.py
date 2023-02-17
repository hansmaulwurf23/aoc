import datetime

begin_time = datetime.datetime.now()

program = []
with open('./input.txt') as f:
    program = [l.rstrip() for l in f.readlines() if l.strip()]


def run(program, registers):
    pc = 0
    while pc < len(program):
        cmd, args = program[pc].split(' ', maxsplit=1)

        if cmd == 'hlf':
            registers[args] //= 2
        elif cmd == 'tpl':
            registers[args] *= 3
        elif cmd == 'inc':
            registers[args] += 1
        elif cmd == 'jmp':
            pc = pc + int(args)
            continue
        elif cmd == 'jie':
            r, offset = args.split(', ')
            if registers[r] % 2 == 0:
                pc += int(offset)
                continue
        elif cmd == 'jio':
            r, offset = args.split(', ')
            if registers[r] == 1:
                pc += int(offset)
                continue
        else:
            raise f"unsupported cmd {cmd} in line {program[pc]}"

        pc += 1

    return registers

registers = run(program, {'a': 0, 'b': 0})
print(f'part 1: {registers["b"]}')
registers = run(program, {'a': 1, 'b': 0})
print(f'part 2: {registers["b"]}')
print(datetime.datetime.now() - begin_time)
