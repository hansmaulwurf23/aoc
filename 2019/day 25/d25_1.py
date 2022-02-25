import datetime
import itertools

from aintcode import InteractiveIntCodeMachine

begin_time = datetime.datetime.now()


def print_output(output):
    for o in output:
        if 0 <= o <= 255:
            print(chr(o), end='')
        else:
            print(o)

    return output


def convert_output(output):
    return ''.join([chr(o) for o in output])


def convert_input(input):
    return list(map(lambda c: ord(c), input)) + [10]


with open('./input.txt') as f:
    program = [int(x) for x in f.readlines()[0].split(',')]

vm = InteractiveIntCodeMachine(program.copy(), [])

collect_script = """south
south
take tambourine
north
north
west
south
take polygon
north
east
north
west
take boulder
east
north
take manifold
north
take hologram
south
west
take fuel cell
south
east
south
take fixed point
north
west
north
north
take wreath
east
east"""

print_output(vm.run_to_command(convert_input(collect_script)))

inventory = ['tambourine', 'hologram', 'fuel cell', 'wreath', 'boulder', 'fixed point', 'manifold', 'polygon']
cur_inv = inventory.copy()
output = convert_output(vm.run_to_command(convert_input('north')))

for length in range(len(inventory) - 1, 0, -1):
    cmds = []
    for invs in itertools.combinations(inventory, length):
        for d in [d for d in cur_inv if d not in invs]:
            cmds.append(f'drop {d}')

        for n in [n for n in invs if n not in cur_inv]:
            cmds.append(f'take {n}')

        cmds.append('inv')
        cmds.append('north')
        output = convert_output(vm.run_to_command(convert_input('\n'.join(cmds))))
        print(output)
        if output.find('Alert!') == -1:
            break
        cur_inv = list(invs)

# print_output(vm.run_to_command([]))
# cmd = ''
# while True:
#     cmd = input('> ')
#     if cmd == 'quit':
#         break
#     print_output(vm.run_to_command(convert_input(cmd)))

print(datetime.datetime.now() - begin_time)
