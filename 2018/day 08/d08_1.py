import datetime
from collections import deque

begin_time = datetime.datetime.now()


def get_metadata(data):
    sum = 0
    no_children = data.popleft()
    no_metadata = data.popleft()
    for c in range(no_children):
        sum += get_metadata(data)

    for m in range(no_metadata):
        sum += data.popleft()

    return sum

with open('./input.txt') as f:
    print(get_metadata(deque(map(int, f.readlines()[0].rstrip().split(' ')))))

print(datetime.datetime.now() - begin_time)
