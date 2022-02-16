import datetime
import re
from collections import deque

begin_time = datetime.datetime.now()


def play(players, last_marble):
    scores = [0] * players
    field = deque([0, 1])
    cur_player = 0
    for next_marble in range(2, last_marble + 1):
        if next_marble % 23 == 0:
            scores[cur_player] += next_marble
            field.rotate(-7)
            scores[cur_player] += field.popleft()
            field.rotate(1)
        else:
            field.rotate(1)
            field.appendleft(next_marble)

        cur_player = (cur_player + 1) % players

    return max(scores)

with open('./input.txt') as f:
    while line := f.readline().rstrip():
        players, last_marble = map(int, re.match(r'(\d+) players; last marble is worth (\d+) points', line).groups())
        print(f'{line}: {play(players, last_marble * 100)}')

print(datetime.datetime.now() - begin_time)
