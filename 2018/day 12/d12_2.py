import datetime
from collections import defaultdict

begin_time = datetime.datetime.now()

def pots_s(pots):
    return ''.join(['#' if pots[i] else '.' for i in sorted(pots.keys())])


def pot_val(pots):
    return sum([i if pots[i] else 0 for i in pots.keys()])


def neighbors(pots, idx):
    return tuple([pots[i] if i in pots else 0 for i in range(idx - 2, idx + 3)])


def pattern(pots):
    return tuple([pots[i] for i in sorted(pots.keys())])


def cycle(pots, rules):
    new_pots = defaultdict(lambda: 0)
    had_one = False
    for idx in range(min(pots.keys()) - 2, max(pots.keys()) + 3):
        hood = neighbors(pots, idx)
        new_val = rules[hood] if hood in rules else 0
        if new_val or had_one:
            new_pots[idx] = new_val
            had_one = True

    for i in range(max(new_pots.keys()), -1, -1):
        if new_pots[i]:
            break
        del new_pots[i]

    return new_pots


with open('./input.txt') as f:
    lines = [l.rstrip() for l in f.readlines()]
    pots = defaultdict(lambda: 0)
    pots = {idx:(1 if c == '#' else 0) for idx, c in enumerate(lines[0].replace('initial state: ',''))}
    rules = dict()
    for rline in lines[2:]:
        rules[tuple(1 if c == '#' else 0 for c in rline[0:5])] = 1 if rline[-1] == '#' else 0

generations = 50000000000
last_pattern = None
last_val = None
g = 0
while True:
    pots = cycle(pots, rules)
    g += 1
    new_pattern = pattern(pots)
    new_val = pot_val(pots)
    if last_pattern is not None and last_pattern == new_pattern:
        break
    last_pattern = new_pattern
    last_val = new_val


print(f'{str(20).rjust(3)} {pots_s(pots)} {min(pots.keys())} {max(pots.keys())} {pot_val(pots)}')
print((generations - g) * (new_val - last_val) + pot_val(pots))

print(datetime.datetime.now() - begin_time)
