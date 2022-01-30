import datetime
from collections import defaultdict

from aopython import ceildiv

begin_time = datetime.datetime.now()


def calc_ingredient_amount(reactions, product, need_amount, leftovers):
    if product in leftovers.keys():
        if leftovers[product] >= need_amount:
            leftovers[product] -= need_amount
            return 0
        else:
            need_amount -= leftovers[product]
            del leftovers[product]

    reaction = reactions[product]
    multiplier = ceildiv(need_amount, reaction['amount'])
    if leftover := multiplier * reaction['amount'] - need_amount:
        leftovers[product] += leftover
    ore_amount = 0
    for ing_data in reaction['ingredients']:
        ingredient, ing_amount = ing_data
        # print(f'i need {multiplier * ing_amount} of {ingredient} / leftovers: {dict(leftovers)}')
        if ingredient == 'ORE':
            ore_amount += (multiplier * ing_amount)
        else:
            ore_amount += calc_ingredient_amount(reactions, ingredient, multiplier * ing_amount, leftovers)

    return ore_amount


reactions = dict()
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        ingredients, product = line.split(' => ')
        amount, elem = product.split(' ')
        amount = int(amount)
        reactions[elem] = {'amount': amount, 'ingredients': []}
        for ingredient in ingredients.split(', '):
            amount, ing = ingredient.split(' ')
            amount = int(amount)
            reactions[elem]['ingredients'].append((ing, amount))

ore_per_fuel = calc_ingredient_amount(reactions, 'FUEL', 1, defaultdict(lambda : 0))
ore = ore_per_fuel
fuel = (1000000000000 // ore_per_fuel)
lastfuel = -1
while ore < 1000000000000 and lastfuel != fuel:
    ore = calc_ingredient_amount(reactions, 'FUEL', fuel, defaultdict(lambda : 0))
    ore_per_fuel = ore / fuel
    lastfuel = fuel
    fuel = int(1000000000000 / ore_per_fuel)
    print(fuel, ore, ore_per_fuel)

print(fuel)
print(datetime.datetime.now() - begin_time)
