import datetime

begin_time = datetime.datetime.now()

digits = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

dx, dy = 1, 1


def process(cmds, dx, dy):
    for cmd in cmds:
        if cmd == 'U':
            dy = dy - 1 if dy > 0 else 0
        if cmd == 'L':
            dx = dx - 1 if dx > 0 else 0
        if cmd == 'R':
            dx = dx + 1 if dx < 2 else 2
        if cmd == 'D':
            dy = dy + 1 if dy < 2 else 2

    return dx, dy

with open('./input.txt') as f:
    while line := f.readline().strip():
        dx, dy = process(line, dx, dy)
        print(digits[dy][dx], end='')

print('')
print(datetime.datetime.now() - begin_time)
