import datetime
from functools import reduce

begin_time = datetime.datetime.now()
MAX = {'red': 12, 'green': 13, 'blue': 14}

with open('./input.txt') as f:
    id_sum, color_sum = 0, 0
    while line := f.readline().rstrip():
        gameID, rounds = line.split(': ')
        gameID = int(gameID.replace('Game ', ''))
        invalid, max_amount = False, {'red': 0, 'green': 0, 'blue': 0}
        for amount, color in [_.split(' ') for _ in [cinfo for rnd in rounds.split('; ') for cinfo in rnd.split(', ')]]:
            amount = int(amount)
            if amount > MAX[color]:
                invalid = True
            max_amount[color] = max(max_amount[color], amount)
        color_sum += reduce(lambda x, y: x * y, max_amount.values())
        if not invalid:
            id_sum += gameID

    print(f'part 1: {id_sum}')
    print(f'part 2: {color_sum}')

print(datetime.datetime.now() - begin_time)
