import datetime

begin_time = datetime.datetime.now()
cmds = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        c, v = line.split(' ')
        cmds.append((c, int(v)))


def part1(cmds):
    moves = {
        'forward': lambda p, x: (p[0] + x, p[1]),
        'up': lambda p, x: (p[0], p[1] + x),
        'down': lambda p, x: (p[0], p[1] - x),
    }
    x, y = 0, 0
    for c, v in cmds:
        x, y = moves[c]((x, y), v)
    return x * -y


def part2(cmds):
    moves = {
        'forward': lambda p, x, a: (p[0] + x, p[1] + (a * x), a),
        'up': lambda p, x, a: (*p, a + x),
        'down': lambda p, x, a: (*p, a - x),
    }
    x, y, a = 0, 0, 0
    for c, v in cmds:
        x, y, a = moves[c]((x, y), v, a)
    return x * -y


print(f'part 1: {part1(cmds)}')
print(f'part 2: {part2(cmds)}')
print(datetime.datetime.now() - begin_time)
