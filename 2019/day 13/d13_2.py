import datetime
from intcode import IntCodeMachine
from aopython import cmp

begin_time = datetime.datetime.now()

tile_map = {0: ' ', 1: '#', 2: 'X', 3: '_', 4: 'O'}


def print_map(outputs):
    fx = max([min([outputs[i] for i in range(0, len(outputs), 3)]), 0])
    tx = max([outputs[i] for i in range(0, len(outputs), 3)])
    fy = min([outputs[i] for i in range(1, len(outputs), 3)])
    ty = max([outputs[i] for i in range(1, len(outputs), 3)])

    lines = []
    for y in range(fy, ty + 1):
        lines.append([''] * (tx - fx + 1))

    for i in range(0, len(outputs), 3):
        x, y, t = outputs[i:i + 3]
        if x >= 0 and t in tile_map.keys():
            lines[y][x] = tile_map[t]

    for l in lines:
        print(''.join(l))


with open('./input.txt') as f:
    program = [int(x) for x in f.readlines()[0].split(',')]

# magic coin
program[0] = 2

vm = IntCodeMachine(program)
paddle_pos = 0
joystick_position = 0
score = 0
while not vm.terminated:
    out = vm.run_to_n_outputs([joystick_position], 3)
    if len(out) < 3:
        continue

    x, y, t = out
    if x == -1 and y == 0:
        score = t
    elif t == 3:
        # position of paddle
        paddle_pos = x
    elif t == 4:
        # position of ball
        joystick_position = cmp(x, paddle_pos)

print(score)
print(datetime.datetime.now() - begin_time)
