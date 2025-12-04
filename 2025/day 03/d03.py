import datetime
begin_time = datetime.datetime.now()

def max_val(digits, rest):
    mx = max(digits[:len(digits) - rest + 1])
    return mx * (10 ** (rest - 1)) + (max_val(digits[digits.index(mx) + 1:], rest - 1) if rest > 1 else 0)


p1, p2 = 0, 0
with open('./input.txt') as f:
    while line := list(map(int, f.readline().rstrip())):
        p1 += max_val(line, 2)
        p2 += max_val(line, 12)

print(f'part 1: {p1}')
print(f'part 2: {p2}')
assert p1 in (17092, 357)
assert p2 in (170147128753455, 3121910778619)
print(datetime.datetime.now() - begin_time)
