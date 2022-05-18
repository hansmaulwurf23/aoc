import datetime

begin_time = datetime.datetime.now()

digits = [[None, None, '1', None, None],
          [None, '2', '3', '4', None],
          ['5', '6', '7', '8', '9'],
          [None, 'A', 'B', 'C', None],
          [None, None, 'D', None, None]]

MAX = 4
dx, dy = 0, 2


def process(cmds, dx, dy):
    for cmd in cmds:
        oldx, oldy = dx, dy
        if cmd == 'U':
            dy = dy - 1 if dy > 0 else 0
        if cmd == 'L':
            dx = dx - 1 if dx > 0 else 0
        if cmd == 'R':
            dx = dx + 1 if dx < MAX else MAX
        if cmd == 'D':
            dy = dy + 1 if dy < MAX else MAX

        if digits[dy][dx] is None:
            dx, dy = oldx, oldy

    return dx, dy


with open('./input.txt') as f:
    while line := f.readline().strip():
        dx, dy = process(line, dx, dy)
        print(digits[dy][dx], end='')

print('')
print(datetime.datetime.now() - begin_time)
