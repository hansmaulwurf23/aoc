import datetime
from collections import Counter

begin_time = datetime.datetime.now()

left, right = [], []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        a, b = list(map(int, line.split()))
        left.append(a)
        right.append(b)

print(f'part 1: {sum([abs(a - b) for a, b in zip(sorted(left), sorted(right))])}')
right = Counter(right)
print(f'part 2: {sum([l * right[l] for l in left])}')
print(datetime.datetime.now() - begin_time)
