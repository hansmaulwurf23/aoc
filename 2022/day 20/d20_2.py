import datetime
from collections import deque

begin_time = datetime.datetime.now()
values = deque()
decryption_key = 811589153

def mix():
    global values, indexes
    for i in range(length):
        # since numbers need to be processed in appearing order we need to find the current offset
        offset = indexes.index(i)
        # rotate index and value to back
        indexes.rotate(-offset - 1)
        values.rotate(-offset - 1)
        # remove from back of deque, rotate to front and re-append
        val = values.pop()
        values.rotate(-val)
        values.append(val)
        # update the index position as well
        idx = indexes.pop()
        indexes.rotate(-val)
        indexes.append(idx)


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        values.append(int(line) * 811589153)

length = len(values)
indexes = deque(range(length))
for run in range(10):
    mix()

offset = values.index(0)
print(sum([values[(offset + (i + 1) * 1000) % length] for i in range(3)]))
print(datetime.datetime.now() - begin_time)
