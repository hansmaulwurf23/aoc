import datetime
from collections import Counter
begin_time = datetime.datetime.now()


def is_valid(phrase):
    c = Counter(phrase.split(' '))
    return c.most_common(1)[0][1] == 1


with open('./input.txt') as f:
    print(len([1 for p in f.readlines() if is_valid(p.rstrip())]))


print(datetime.datetime.now() - begin_time)
