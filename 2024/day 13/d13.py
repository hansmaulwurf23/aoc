import datetime
import re

from aopython import int_solve

begin_time = datetime.datetime.now()


def min_tokens(btn_a, btn_b, prize):
    a, b = int_solve([[btn_a[0], btn_b[0]], [btn_a[1], btn_b[1]]], prize)
    if a is not None and b is not None:
        return a * 3 + b
    return None


configs = []
with open('./input.txt') as f:
    lines = list(map(lambda l: l.rstrip(), f.readlines()))

    for info in [lines[i:i + 4] for i in range(0, len(lines), 4)]:
        btn_a = list(map(int, re.findall(r'(\d+)', info[0])))
        btn_b = list(map(int, re.findall(r'(\d+)', info[1])))
        prize = list(map(int, re.findall(r'(\d+)', info[2])))
        configs.append((btn_a, btn_b, prize))

s1 = 0
s2 = 0
for c in configs:
    tokens = min_tokens(*c)
    if tokens is not None:
        s1 += tokens
    c[-1][0] += 10000000000000
    c[-1][1] += 10000000000000
    tokens = min_tokens(*c)
    if tokens is not None:
        s2 += tokens

print(s1)
print(s2)
assert s1 in (29201, 480)
assert s2 in (104140871044942, 875318608908)
print(datetime.datetime.now() - begin_time)
