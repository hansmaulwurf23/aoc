import datetime
from itertools import combinations

begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    sum = 0
    while line := f.readline().rstrip():
        numbers = list(sorted(map(int, line.split('\t')), reverse=True))
        sum += [x // y for (x, y) in combinations(numbers[:], 2) if x % y == 0][0]

print(sum)
print(datetime.datetime.now() - begin_time)
