import datetime
from aintcode import InteractiveIntCodeMachine
begin_time = datetime.datetime.now()


def print_output(output):
    for o in output:
        if 0 <= o <= 255:
            print(chr(o), end='')
        else:
            print(o)

    return output


def convert_input(input):
    return list(map(lambda c: ord(c), input)) + [10]


with open('./input.txt') as f:
    program = [int(x) for x in f.readlines()[0].split(',')]

vm = InteractiveIntCodeMachine(program.copy(), [])
cmd = ''
while True:
    print_output(vm.run_to_command(convert_input(cmd)))
    cmd = input('> ')
    if cmd == 'quit':
        break

print(datetime.datetime.now() - begin_time)
