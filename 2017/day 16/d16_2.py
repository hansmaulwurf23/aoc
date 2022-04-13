import datetime
import re
from collections import deque

begin_time = datetime.datetime.now()

progs = deque(range(16))


def dance(moves, progs):
    for move in moves:
        if move[0] == 's':
            n = int(move[1:])
            progs.rotate(n)
        elif move[0] == 'x':
            a, b = map(int, re.findall(r'\d+', move))
            progs[b], progs[a] = progs[a], progs[b]
        elif move[0] == 'p':
            a, b = map(lambda c: progs.index(ord(c) - ord('a')), [move[1], move[3]])
            progs[b], progs[a] = progs[a], progs[b]

    return progs


with open('./input.txt') as f:
    moves = f.readlines()[0].rstrip().split(',')

seen = {tuple(progs)}
rest_runs = 1000000000
run = 0
repeat_at = None
while rest_runs:
    progs = dance(moves, progs)
    rest_runs -= 1
    run += 1
    if repeat_at is None:
        if tuple(progs) in seen:
            print(f'repeat at {run}')
            rest_runs = rest_runs % run
            repeat_at = run
        else:
            seen.add(tuple(progs))


print(''.join(map(lambda p: chr(p + ord('a')), progs)))
print(datetime.datetime.now() - begin_time)
