import datetime
from collections import deque
from itertools import zip_longest

begin_time = datetime.datetime.now()
SIZE, ID = range(2)

def chksum(disk):
    chksm, offset = 0, 0
    for blocks, id in disk:
        for b in [b for b in range(blocks) if id is not None]:
            chksm += ((offset + b) * id)
        offset += blocks
    return chksm


disk = deque([])
new_disk = deque([])
with open('./input.txt') as f:
    line = list(map(int, f.readline().rstrip()))
    # line = list(map(int, '12345'))
    for id, (used, free) in enumerate([(a, b) for a, b in zip_longest(line[::2], line[1::2])]):
        disk.append([used, id])
        disk.append([free, None])

# make a backup for part two ;-)
spare_disk = deque(disk)

# remove last free space entry
disk.pop()
new_disk.append(disk.popleft())

# left ALWAYS free, right end ALWAYS used
while disk:
    used, id = disk.pop()
    if not disk:
        new_disk.append([used, id])
        break
    free, _ = disk.popleft()

    if used <= free:
        new_disk.append([used, id])
        if used < free:
            disk.appendleft([free - used, None])
        else:
            if disk:
                new_disk.append(disk.popleft())
        # trailing free space
        if disk:
            disk.pop()
    else:
        new_disk.append([free, id])
        if disk:
            new_disk.append(disk.popleft())
        disk.append([used - free, id])

print(f'part 1: {chksum(new_disk)}')

disk = spare_disk
# remove last free space entry
disk.pop()
free_idx, used_idx = 1, len(disk) - 1
moved_idx = set()
while used_idx >= 0:
    used, id = disk[used_idx]
    for i in [i for i in range(free_idx, used_idx) if disk[i][ID] is None]:
        free, _ = disk[i]
        if free >= used:
            disk[i] = [used, id]
            moved_idx.add(id)
            disk[used_idx][ID] = None
            if free > used:
                disk.insert(i + 1, [free - used, None])
                used_idx += 1
                free_idx = i + 1 if free_idx == i else free_idx
            break
    used_idx -= 1
    while disk[used_idx][ID] is None or disk[used_idx][ID] in moved_idx:
        used_idx -= 1

print(f'part 2: {chksum(disk)}')
print(datetime.datetime.now() - begin_time)
