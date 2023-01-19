import datetime

begin_time = datetime.datetime.now()
registers = {'a':0, 'b':0, 'c':0, 'd':0}
code = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        code.append(line.split(' ', maxsplit=1))


def run_raw(initial_a, max_out):
    registers['a'] = initial_a
    pc = 0
    last_out = None
    outs = []
    while pc < len(code):
        cmd, args = code[pc]
        # print(cmd, args)

        if cmd == 'inc':
            registers[args] += 1
        elif cmd == 'dec':
            registers[args] -= 1
        elif cmd == 'jnz':
            x, y = args.split(' ')
            pc += int(y) if (x.isnumeric() and int(x)) or (x in registers and registers[x]) else 1
            continue
        elif cmd == 'cpy':
            x, y = args.split(' ')
            if x.isnumeric():
                registers[y] = int(x)
            else:
                registers[y] = registers[x]
        elif cmd == 'out':
            #print(registers[args])
            outs.append(registers[args])
            if max_out is not None:
                if len(outs) == max_out:
                    return outs
            if last_out != registers[args]:
                last_out = registers[args]
            else:
                 #print(f'same output {last_out}')
                 return outs

        pc += 1


def run_fast(initial_a, max_out):
    outs = []
    a = initial_a
    d = a + 182 * 14
    while True:
        a = d
        first = True
        while first or a:
            first = False
            b = a
            a = 0
            c = 2
            while b:
                b -= 1
                c -= 1
                if not c:
                    a += 1
                    c = 2

            b = 2
            while c:
                b -= 1
                c -= 1

            # NOOP[27]
            outs.append(b)
            if len(outs) >= 2 and outs[-1] == outs[-2]:
                return outs
            if len(outs) == max_out:
                return outs


max_out = 100
# compare_mode was used to make sure the transpilling and simplifying was done correctly
compare_mode = False
for a in range(500):
    if compare_mode:
        res1 = tuple(run_raw(a, max_out))
        res2 = tuple(run_fast(a, max_out))
        if res1 != res2:
            print('res differ!')
        else:
            if len(res1) == max_out:
                print(f'{a} {res1}')
                break
    else:
        res = run_fast(a, max_out)
        if len(res) == max_out:
            print(f'{a}')
            break

print(datetime.datetime.now() - begin_time)
