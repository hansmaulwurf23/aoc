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
        print(f'i need {multiplier * ing_amount} of {ingredient} / leftovers: {dict(leftovers)}')
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

print(calc_ingredient_amount(reactions, 'FUEL', 1, defaultdict(lambda : 0)))
print(datetime.datetime.now() - begin_time)
