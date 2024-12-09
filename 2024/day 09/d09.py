import datetime
from collections import deque, defaultdict
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


def defrag_blockwise(orgdisk):
    disk, new_disk = deque(orgdisk), []

    # remove last free space entry
    disk.pop()
    new_disk.append(disk.popleft())

    # left end ALWAYS free, right end ALWAYS used
    while disk:
        used, id = disk.pop()
        if not disk:
            new_disk.append([used, id])
            break

        free, _ = disk.popleft()

        if used <= free:
            # whole block can be moved
            new_disk.append([used, id])
            if used < free:
                # add rest of free space
                disk.appendleft([free - used, None])
            else:
                # directly add next used block to make sure left end is a free block
                if disk: new_disk.append(disk.popleft())
            # trailing free space
            if disk: disk.pop()
        else:
            new_disk.append([free, id])
            if disk: new_disk.append(disk.popleft())
            disk.append([used - free, id])

    return new_disk


def defrag_filewise(orgdisk):
    disk = list(orgdisk)
    free_idx, used_idx = 1, len(disk) - 2
    inserts = defaultdict(list)
    while used_idx >= free_idx:
        used, id = disk[used_idx]
        for i in [i for i in range(free_idx, used_idx, 2) if disk[i][ID] is None]:
            free, _ = disk[i]
            if free >= used:
                disk[used_idx][ID] = None

                if free == used:
                    # replace with file
                    disk[i][ID] = id
                    free_idx = i + 2 if free_idx == i else free_idx
                else:
                    # update free space and store insert for later
                    inserts[i].append((used, id))
                    disk[i][SIZE] = free - used
                break
        used_idx -= 2

    new_disk = []
    for i, (sz, oid) in enumerate(disk):
        if inserts[i]:
            new_disk.extend(inserts[i])
        if sz:
            new_disk.append([sz, oid])

    return new_disk

disk = []
with open('./input.txt') as f:
    line = list(map(int, f.readline().rstrip()))
    for id, (used, free) in enumerate([(a, b) for a, b in zip_longest(line[::2], line[1::2])]):
        disk.append([used, id])
        disk.append([free, None])

p1 = chksum(defrag_blockwise(disk))
print(f'part 1: {p1}')
assert p1 in (6446899523367, 1928)
p2 = chksum(defrag_filewise(disk))
print(f'part 2: {p2}')
assert p2 in (6478232739671, 2858)
print(datetime.datetime.now() - begin_time)
