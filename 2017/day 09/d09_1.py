import datetime
from collections import deque

begin_time = datetime.datetime.now()
score_sum = 0


def process(line):
    in_garbage = False
    group_lvl = 0
    score = 0
    while line:
        c = line.popleft()
        if c == '>':
            in_garbage = False
        elif in_garbage:
            if c == '!':
                line.popleft()
            continue
        elif c == '<':
            in_garbage = True
        elif c == '{':
            group_lvl += 1
        elif c == '}':
            score += group_lvl
            group_lvl -= 1

    return score


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        score_sum += process(deque(line))

print(score_sum)
print(datetime.datetime.now() - begin_time)
