import datetime
import re

begin_time = datetime.datetime.now()

# Reversing the rotate_based op needs some mapping
# Pos	 Rot  NewPos  RevRot
# 0	     1    1       7
# 1	     2    3       6
# 2	     3    5       5
# 3	     4    7       4
# 4	     6    2       2
# 5	     7    4       1
# 6	     0    6       0
# 7	     1    0       7
REV_ROT_BASE_MAP = {1: 7, 3: 6, 5: 5, 7: 4, 2: 2, 4: 1, 6: 0, 0: 7}

def swap_positions(pwd, x, y):
    pwd[x], pwd[y] = pwd[y], pwd[x]
    return pwd


def swap_letter(pwd: str, x, y):
    for i, c in enumerate(pwd):
        if c == x:
            pwd[i] = y
        elif c == y:
            pwd[i] = x

    return pwd


def reverse_positions(pwd: str, x: int, y: int):
    for l in range((y - x) // 2 + 1):
        pwd[x + l], pwd[y - l] = pwd[y - l], pwd[x + l]

    return pwd


def rotate(pwd, dir, x):
    l = len(pwd)
    i = int(x) if isinstance(x, str) else x  # polymorphism done right :D
    if dir == 'right':
        return pwd[l - i:] + pwd[:l - i]
    else:
        return pwd[i:] + pwd[:i]


def move_position(pwd: str, x: int, y: int):
    c = pwd[x]
    pwd = pwd[:x] + pwd[x + 1:]
    pwd = pwd[:y] + [c] + pwd[y:]
    return pwd


def calc_shift_from_base(pos):
    return pos + (2 if pos >= 4 else 1)


def rotate_based(pwd, c):
    idx = pwd.index(c)
    return rotate(pwd, 'right', idx + (2 if idx >= 4 else 1))


def load_commands(filename):
    with open(filename, 'r') as f:
        return list([l.rstrip() for l in f.readlines()])


def run_commands(pwd, commands, reverse=False):
    commands = reversed(commands) if reverse else commands
    pwd = list(pwd)

    for command in commands:
        if command.startswith('swap pos'):
            pwd = swap_positions(pwd, *list(map(int, re.findall('\d+', command))))
        elif command.startswith('reverse positions'):
            pwd = reverse_positions(pwd, *list(map(int, re.findall(r'\d+', command))))
        elif m := re.match(r'swap letter (.) with letter (.)', command):
            pwd = swap_letter(pwd, *m.groups())
        elif command.startswith('move pos'):
            args = list(map(int, re.findall(r'\d+', command)))
            if reverse:
                args = reversed(args)
            pwd = move_position(pwd, *args)
        elif m := re.match(r'rotate (left|right) (\d+) step?', command):
            if reverse:
                pwd = rotate(pwd, 'right' if m.groups()[0] == 'left' else 'left', m.groups()[1])
            else:
                pwd = rotate(pwd, *m.groups())
        elif command.startswith('rotate based'):
            if reverse:
                pwd = rotate(pwd, 'right', REV_ROT_BASE_MAP[pwd.index(command[-1])])
            else:
                pwd = rotate_based(pwd, command[-1])
        else:
            print(f'COMMAND NOT MATCHED! {command}')

    return ''.join(pwd)


cmds = load_commands('./input.txt')
print(f'part 1 {run_commands("abcdefgh", cmds)}')
print(f'part 2 {run_commands("fbgdceah", cmds, reverse=True)}')
print(datetime.datetime.now() - begin_time)
