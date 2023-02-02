import datetime

begin_time = datetime.datetime.now()

sample = {
    ('children', 3),
    ('cats', 7),
    ('samoyeds', 2),
    ('pomeranians', 3),
    ('akitas', 0),
    ('vizslas', 0),
    ('goldfish', 5),
    ('trees', 3),
    ('cars', 2),
    ('perfumes', 1)}

sue_patterns = dict()
with open('./input.txt') as f:
    def convert(inv):
        item, amount  = inv.split(': ')
        amount = int(amount)
        return item, amount

    while line := f.readline().rstrip():
        name, inventory = line.split(': ', maxsplit=1)
        sue_idx = int(name[3:])
        inventory = set(map(lambda inv: convert(inv), inventory.split(', ')))
        sue_patterns[sue_idx] = inventory

for sue_idx, inventory in sue_patterns.items():
    same = sample & inventory
    if len(same) == len(inventory):
        print(f'part 1: {sue_idx}: {same}')
        break

less_thans = {('cats', 7), ('trees', 3)}
more_thans = {('pomeranians', 3), ('goldfish', 5)}
sample -= less_thans
sample -= more_thans
less_thans = {k: v for k, v in less_thans}
more_thans = {k: v for k, v in more_thans}

for sue_idx, inventory in sue_patterns.items():
    valids = len(sample & inventory)
    for item, amount in inventory:
        if item in less_thans and less_thans[item] < amount:
            valids += 1
        if item in more_thans and more_thans[item] > amount:
            valids += 1

    if valids == len(inventory):
        print(f'part 2: {sue_idx}: {inventory}')
        break

print(datetime.datetime.now() - begin_time)
