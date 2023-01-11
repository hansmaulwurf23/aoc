import datetime

begin_time = datetime.datetime.now()
registers = {'a': 12, 'b': 0, 'c': 0, 'd': 0}
TOGGLE_MAP = {'dec': 'inc', 'inc': 'dec', 'jnz': 'cpy', 'cpy': 'jnz', 'tgl': 'inc'}
code = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        code.append(line.split(' ', maxsplit=1))

pc = 0
while pc < len(code):
    cmd, args = code[pc]
    # print(cmd, args)

    if cmd == 'inc':
        if args in registers:
            registers[args] += 1
    elif cmd == 'dec':
        if args in registers:
            registers[args] -= 1
    elif cmd == 'jnz':
        x, y = args.split(' ')
        offset = int(y) if y.lstrip('-').isnumeric() else registers[y]
        pc += offset if (x.isnumeric() and x) or registers[x] else 1
        continue
    elif cmd == 'cpy':
        x, y = args.split(' ')
        registers[y] = int(x) if x.lstrip('-').isnumeric() else registers[x]
    elif cmd == 'tgl':
        if 0 <= pc + registers[args] < len(code):
            print(f'TOOGLE {pc + registers[args]} from {code[pc + registers[args]]} to '
                  f'{TOGGLE_MAP[code[pc + registers[args]][0]]}')
            code[pc + registers[args]][0] = TOGGLE_MAP[code[pc + registers[args]][0]]

    pc += 1

print(registers['a'])
print(datetime.datetime.now() - begin_time)
