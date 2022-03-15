import datetime
from collections import deque

begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    lengths = list(map(int, f.readlines()[0].rstrip().split(',')))

# numbers = deque(range(256))
NUMLEN = 256
numbers = deque(range(NUMLEN))
# lengths = [3, 4, 1, 5]
cur_pos, skip_size = 0, 0

for l in lengths:
    new_numbers = deque()
    for _ in range(l):
        new_numbers.appendleft(numbers.popleft())
    while numbers:
        new_numbers.append(numbers.popleft())

    new_numbers.rotate(-l - skip_size)
    cur_pos = (cur_pos + skip_size + l) % NUMLEN
    skip_size += 1
    numbers = new_numbers

numbers.rotate(cur_pos)
print(numbers[0] * numbers[1])
print(datetime.datetime.now() - begin_time)
