import datetime
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


with open('./input.txt') as f:
    lines = f.readlines()
    idx, pair = 0, 1
    righties = 0
    while idx < len(lines):
        l, r = eval(lines[idx]), eval(lines[idx + 1])
        if compare(l, r):
            righties += pair
        idx += 3
        pair += 1

print(righties)
print(datetime.datetime.now() - begin_time)
