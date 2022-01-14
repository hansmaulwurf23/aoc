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
        decks[i].append(int(line))


def play(deck_a, deck_b):
    prev_decks = set()
    while deck_a and deck_b:
        if tuple([tuple(deck_a), tuple(deck_b)]) in prev_decks:
            return 0, deck_a
        else:
            prev_decks.add(tuple([tuple(deck_a), tuple(deck_b)]))

        (a, b) = deck_a.popleft(), deck_b.popleft()

        if len(deck_a) >= a and len(deck_b) >= b:
            sub_game_winner, _ = play(deque(tuple(deck_a)[:a]), deque(tuple(deck_b)[:b]))
            deck_a.extend([a, b]) if sub_game_winner == 0 else deck_b.extend([b, a])
        elif a > b:
            deck_a.extend([a, b])
        else:
            deck_b.extend([b, a])

    return (0, deck_a) if deck_a else (1, deck_b)


def calc_score(deck):
    score = 0
    for i in range(len(deck), 0, -1):
        score += (i * deck.popleft())

    return score


winner, winner_deck = play(decks[0].copy(), decks[1].copy())
print(calc_score(winner_deck))
print(datetime.datetime.now() - begin_time)
