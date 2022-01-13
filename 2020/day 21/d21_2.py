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

todos = set([allg for allg, ings in all_from_ing.items() if len(ings) == 1])
while len(todos):
    curAllg = todos.pop()
    curIngs = all_from_ing[curAllg]
    for allg in [a for a in all_from_ing.keys() if a != curAllg]:
        if curIngs & all_from_ing[allg]:
            all_from_ing[allg] -= curIngs
            if len(all_from_ing[allg]) == 1:
                todos.add(allg)

# the one and only canonical dangerour ingredients list
cdil = []
for allg in sorted(all_from_ing.keys()):
    cdil.extend(list(all_from_ing[allg]))
print(','.join(cdil))
print(datetime.datetime.now() - begin_time)
