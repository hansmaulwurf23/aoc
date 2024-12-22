import datetime
from collections import defaultdict

begin_time = datetime.datetime.now()


with open('./input.txt') as f:
    secret_numbers = list(map(int, f.read().splitlines()))

# secret_numbers = [123]
p1, bananas = 0, defaultdict(int)
for i, s in enumerate(secret_numbers):
    prices, diff, change_patterns = [], [], {}
    prices.append(s % 10)
    for r in range(2000):
        s = ((s << 6) ^ s) & 16777215
        s = ((s >> 5) ^ s) & 16777215
        s = ((s << 11) ^ s) & 16777215
        prices.append(s % 10)
        diff.append(prices[-1] - prices[-2])
        if r > 2:
            pattern = tuple(diff[-4:])
            if pattern not in change_patterns:
                change_patterns[pattern] = prices[-1]
    p1 += s
    for pattern, price in change_patterns.items():
        bananas[pattern] += price

print(f'part 1: {p1}')
assert p1 in (16999668565, 37327623, 37990510)
p2 = max(bananas.values())
print(f'part 2: {p2}')
assert p2 in (1898, 23)
print(datetime.datetime.now() - begin_time)
