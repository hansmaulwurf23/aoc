import datetime
from collections import deque

from aopython import vector_add

begin_time = datetime.datetime.now()
# DIMX, DIMY, fname, cap = 6, 6, './example.txt', 12
DIMX, DIMY, fname, cap = 70, 70, './input.txt', 1024
DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))

def in_grid(x, y):
    return 0 <= x <= DIMX and 0 <= y <= DIMY

def bfs(start, end, cap):
    q = deque()
    q.append((start, 0))
    seen = set()

    while q:
        cur, steps = q.popleft()

        if cur == end:
            return steps

        for nxt in [tuple(vector_add(cur, d)) for d in DIRS]:
            if nxt not in seen and in_grid(*nxt) and (nxt not in bytes or bytes[nxt] > cap):
                q.append((nxt, steps + 1))
                seen.add(nxt)

    return False

with open(fname) as f:
    bytes = {tuple(map(int, l.split(','))): i+1 for i, l in enumerate(f.read().splitlines())}

start, end = (0, 0), (DIMX, DIMY)
p1 = bfs(start, end, cap)
print(f'part 1: {p1}')
assert p1 in (272, 22)

lo, hi = 0, len(bytes)
while True:
    cap = lo + ((hi - lo) // 2)
    if not bfs(start, end, cap):
        hi = cap
    else:
        lo = cap

    if lo + 1 == hi:
        break

print(f"part 2: {','.join(map(str, list(filter(lambda b: bytes[b] == hi, bytes))[0]))}")
print(datetime.datetime.now() - begin_time)
