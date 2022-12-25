import datetime
from functools import reduce
from itertools import zip_longest

from aopython import sign

begin_time = datetime.datetime.now()
VALUES = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
SYMBOLS = {v: k for k, v in VALUES.items()}


def add(a, b):
    digits, remember = [], 0
    for x, y in zip_longest(reversed(a), reversed(b), fillvalue='0'):
        digits.append(VALUES[x] + VALUES[y] + remember)
        remember = sign(digits[-1]) if abs(digits[-1]) > 2 else 0
        digits[-1] += (-5 * remember)

    return ''.join(reversed(list(map(lambda d: SYMBOLS[d], digits))))


print(reduce(lambda a, b: add(a, b), list([l.rstrip() for l in open('./input.txt').readlines()])))
print(datetime.datetime.now() - begin_time)
