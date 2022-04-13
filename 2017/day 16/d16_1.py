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
    progs = dance(f.readlines()[0].rstrip().split(','), progs)
    # progs = dance(f.readlines()[0].rstrip().split(','), deque(range(5)))

print(''.join(map(lambda p: chr(p + ord('a')), progs)))
print(datetime.datetime.now() - begin_time)
