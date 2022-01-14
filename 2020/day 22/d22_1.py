import datetime
from collections import deque
begin_time = datetime.datetime.now()

decks = [deque(), deque()]

with open('./input.txt') as file:
    i = 0
    while line := file.readline():
        if not line.rstrip():
            i += 1
            continue

        if line.startswith('Player'):
            continue
        decks[i].appendleft(int(line))


def play(deck1, deck2):
    while deck1 and deck2:
        a, b = deck1.pop(), deck2.pop()
        if a > b:
            deck1.extendleft([a, b])
        else:
            deck2.extendleft([b, a])

    return deck1 if deck1 else deck2


def calc_score(deck):
    score = 0
    for i in range(len(deck), 0, -1):
        score += (i * deck.pop())

    return score


print(calc_score(play(*decks)))
print(datetime.datetime.now() - begin_time)
