import datetime
from functools import cache

begin_time = datetime.datetime.now()

@cache
def is_possible(design, stripes):
    if not design:
        return 1
    return sum(is_possible(design[len(s):], stripes) for s in stripes if design.startswith(s))


with open('./input.txt') as f:
    lines = f.read().splitlines()
    stripes, designs = tuple(lines[0].split(', ')), lines[2:]

results = [is_possible(d, stripes) for d in designs]
print(f'part 1: {sum(r > 0 for r in results)}')
print(f'part 2: {sum(r for r in results)}')
print(is_possible.cache_info())
print(datetime.datetime.now() - begin_time)
