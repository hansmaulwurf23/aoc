import datetime
from collections import deque

begin_time = datetime.datetime.now()


def get_metadata(data):
    val = 0
    no_children = data.popleft()
    no_metadata = data.popleft()

    child_vals = dict()
    for c in range(1, no_children + 1):
        child_vals[c] = get_metadata(data)

    if no_children:
        for m in range(no_metadata):
            cidx = data.popleft()
            if cidx in child_vals:
                val += child_vals[cidx]
    else:
        for m in range(no_metadata):
            val += data.popleft()

    return val

with open('./input.txt') as f:
    print(get_metadata(deque(map(int, f.readlines()[0].rstrip().split(' ')))))

print(datetime.datetime.now() - begin_time)
