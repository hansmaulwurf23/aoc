import datetime
import re
from collections import deque

begin_time = datetime.datetime.now()


def play(players, last_marble):
    scores = [0] * players
    field = [0, 1]
    cur_marble_idx = 1
    cur_player = 0
    for next_marble in range(2, last_marble + 1):
        if next_marble % 23 == 0:
            scores[cur_player] += next_marble
            cur_marble_idx = (cur_marble_idx - 7) % len(field)
            scores[cur_player] += field[cur_marble_idx]
            field = field[0:cur_marble_idx] + field[cur_marble_idx+1:]
        else:
            cur_marble_idx = (cur_marble_idx + 2) % len(field)
            field.insert(cur_marble_idx, next_marble)

        cur_player = (cur_player + 1) % players

    return max(scores)

with open('./input.txt') as f:
    while line := f.readline().rstrip():
        players, last_marble = map(int, re.match(r'(\d+) players; last marble is worth (\d+) points', line).groups())
        print(f'{line}: {play(players, last_marble)}')

print(datetime.datetime.now() - begin_time)
