import datetime
from collections import defaultdict

begin_time = datetime.datetime.now()

win_sum = 0
card_counter = defaultdict(int)
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        cardID, infos = line.split(': ')
        cardID = int(cardID.replace('Card ', '').strip())
        card_counter[cardID] += 1
        card_amount = card_counter[cardID]

        winning_numbers, my_numbers = infos.split(' | ')
        winning_numbers = set(winning_numbers.split())
        my_numbers = set(my_numbers.split())
        won_numbers = len(my_numbers.intersection(winning_numbers))
        win_sum += pow(2, won_numbers - 1) if won_numbers else 0
        for i in range(cardID + 1, cardID + won_numbers + 1):
            card_counter[i] += card_amount

print(f'part 1: {win_sum}')
print(f'part 1: {sum(card_counter.values())}')
print(datetime.datetime.now() - begin_time)
