import datetime
from collections import defaultdict

begin_time = datetime.datetime.now()


def is_valid(pages, rules):
    for p_idx, page in enumerate(pages):
        for o_idx, other in enumerate([o for o in pages[p_idx + 1:]]):
            if page in rules[other]:
                return False, (p_idx, o_idx + p_idx + 1)

    return True, None


rules, sum1, sum2 = defaultdict(set), 0, 0
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        pg, bef = map(int, line.split('|'))
        rules[pg].add(bef)

    while line := f.readline().rstrip():
        pages = list(map(int, line.split(',')))
        valid, wrongs = is_valid(pages, rules)
        if valid:
            sum1 += pages[len(pages) // 2]
        else:
            while not valid:
                a, b = wrongs
                pages[a], pages[b] = pages[b], pages[a]
                valid, wrongs = is_valid(pages, rules)
            sum2 += pages[len(pages) // 2]

print(f'part 1: {sum1}')
print(f'part 2: {sum2}')
print(datetime.datetime.now() - begin_time)
