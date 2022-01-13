import datetime
from collections import defaultdict
begin_time = datetime.datetime.now()

all_from_ing = dict()
ingred_counters = defaultdict(int)

with open('./input.txt') as file:
    while line := file.readline().rstrip():
        (ingreds, allergs) = line[0:-1].split(' (contains ')
        ingreds = set(ingreds.split(' '))
        allergs = set(allergs.split(', '))

        for a in allergs:
            if a not in all_from_ing.keys():
                all_from_ing[a] = ingreds.copy()
            else:
                all_from_ing[a] &= ingreds.copy()

        for i in ingreds:
            ingred_counters[i] += 1

daSum = 0
badIngreds = set()
for ingreds in all_from_ing.values():
    badIngreds |= ingreds

for goodIngreds in [i for i in ingred_counters.keys() if i not in badIngreds]:
    daSum += ingred_counters[goodIngreds]

print(daSum)
print(datetime.datetime.now() - begin_time)
