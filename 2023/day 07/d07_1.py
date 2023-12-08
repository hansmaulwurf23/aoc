import datetime
import functools
from collections import Counter
from functools import cmp_to_key

begin_time = datetime.datetime.now()
CARDS, BID, CARDVALS = range(3)
CARD_ORDER = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
(HIGH_CARD, ONE_PAIR, TWO_PAIRS, THREE_OF_A_KIND, FULL_HOUSE,
 FOUR_OF_A_KIND, FIVE_OF_A_KIND) = range(7)
FACE, COUNT = range(2)


@functools.cache
def kind_val(cards):
    c = Counter(cards)
    distinct_cards = len(c)
    top_card = c.most_common(1)[0]
    best_two = c.most_common(2)

    if distinct_cards == 1:
        return FIVE_OF_A_KIND
    elif distinct_cards == 2:
        return FOUR_OF_A_KIND if top_card[COUNT] == 4 else FULL_HOUSE
    elif top_card[COUNT] == 3:
        return THREE_OF_A_KIND
    elif best_two[1][COUNT] == 2:
        return TWO_PAIRS
    elif top_card[COUNT] == 2:
        return ONE_PAIR
    return HIGH_CARD



def order_hands(a, b):
    v1, v2 = kind_val(a[CARDS]), kind_val(b[CARDS])
    if v2 < v1:
        return 1
    elif v1 < v2:
        return -1

    for v1, v2 in zip(a[CARDVALS], b[CARDVALS]):
        if v2 < v1:
            return 1
        elif v1 < v2:
            return -1

    return 0


hands = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        cards, bid = line.split()
        bid, cardvals = int(bid), [CARD_ORDER.index(c) for c in cards]
        hands.append([cards, bid, cardvals])


total_winnings = 0
for rank, (cards, bid, _) in enumerate(sorted(hands, key=cmp_to_key(order_hands))):
    total_winnings += ((rank + 1) * bid)
print(total_winnings)
print(datetime.datetime.now() - begin_time)
