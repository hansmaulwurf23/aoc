from functools import cache
from itertools import permutations
from aopython import vector, vector_add

DIRS = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}
MOVS = {v: k for k, v in DIRS.items()}
num_pad = {'7': (0, 0), '8': (1, 0), '9': (2, 0),
           '4': (0, 1), '5': (1, 1), '6': (2, 1),
           '1': (0, 2), '2': (1, 2), '3': (2, 2),
           None: (0, 3), '0': (1, 3), 'A': (2, 3)}
num_pos = {v: k for k, v in num_pad.items() if k is not None}
dir_pad = {None: (0, 0), '^': (1, 0), 'A': (2, 0),
           '<': (0, 1), 'v': (1, 1), '>': (2, 1)}
dir_pos = {v: k for k, v in dir_pad.items() if k is not None}


def change_count(seq):
    return sum(a != b for a, b in zip(seq, seq[1:]))


def in_pad(x, y, pad):
    return 0 <= x < len(pad[0]) and 0 <= y < len(pad) and pad[y][x] is not None


def padv(x, y, pad):
    return pad[y][x]


def print_diff(seqa, seqb):
    diffstr = ''
    for a, b in zip(seqa, seqb):
        diffstr += ' ' if a == b else '|'
    print(seqa)
    print(diffstr)
    print(seqb)


def run_moves(seq, target_pad, target_pos):
    cur = target_pos['A']
    res = ''
    for s in seq:
        if s == 'A':
            res += padv(*cur, target_pad)
        else:
            cur = vector_add(cur, MOVS[s])
    return res


@cache
def generate_seq(run, max_runs, initial, key):
    pad, positions = (num_pad, num_pos) if run == 0 else (dir_pad, dir_pos)
    cur = pad[initial]
    delta = vector(cur, pad[key])
    dx, dy = delta

    if run == max_runs - 1:
        return abs(dy) + abs(dx) + 1

    if dy == dx == 0:
        return 1

    seq = []
    seq.extend(list('^' if dy < 0 else 'v') * abs(dy))
    seq.extend(list('<' if dx < 0 else '>') * abs(dx))

    seqs = []
    for r in set(permutations(seq)):
        pos = cur
        steps = 0
        for b, c in zip(['A'] + list(r), r):
            steps += generate_seq(run + 1, max_runs, b, c)
            pos = tuple(vector_add(pos, DIRS[c]))
            if pos not in positions:
                break
        else:
            steps += generate_seq(run + 1, max_runs, r[-1], 'A')
            seqs.append(steps)
    return min(seqs)


with open('input.txt', 'r') as f:
    codes = f.read().splitlines()

for part, num_robots in enumerate([3, 26], start=1):
    s = 0
    for code in codes:
        complexity = sum(generate_seq(0, num_robots, initial, key) for initial, key in zip('A' + code, code))
        s += (complexity * int(code[:-1]))
    print(f'part {part}: {s}')

print(248108)
print(303836969158972)
