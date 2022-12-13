import datetime
from functools import cmp_to_key
from itertools import zip_longest

begin_time = datetime.datetime.now()


def compare(l, r):
    if isinstance(l, int) and isinstance(r, int):
        return True if l < r else (None if l == r else False)
    elif isinstance(l, list) and isinstance(r, list):
        for a, b in zip_longest(l, r):
            if a is None:
                return True
            elif b is None:
                return False
            if (v := compare(a, b)) is not None:
                return v
    elif isinstance(l, list):
        return compare(l, [r])
    elif isinstance(r, list):
        return compare([l], r)
    return None


def cmp(l, r):
    return -1 if compare(l, r) else 1


DIV1, DIV2 = [[2]], [[6]]
signals = [DIV1, DIV2]
with open('./input.txt') as f:
    for s in list(map(eval, list(filter(lambda l: l.rstrip(), f.readlines())))):
        signals.append(s)

signals = sorted(signals, key=cmp_to_key(cmp))
print(f'{(signals.index(DIV1) + 1) * (signals.index(DIV2) + 1)}')
print(datetime.datetime.now() - begin_time)
