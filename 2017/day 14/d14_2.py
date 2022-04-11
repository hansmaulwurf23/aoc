import datetime

from knot_hash import knot_hash, knot_hash_hex, hex_hash

begin_time = datetime.datetime.now()
GRID_SIZE = 128

def adjacents(x, y):
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        ax, ay = dx + x, dy + y
        if 0 <= ax < GRID_SIZE and 0 <= ay < GRID_SIZE:
            yield ax, ay


input = 'ljoxqyyw'
# input = 'flqrgnkx'
used = 0
matrix = []
for i in range(GRID_SIZE):
    row_hash = knot_hash(f'{input}-{i}')
    matrix.append([])
    while row_hash:
        byte = row_hash.pop()
        for _ in range(8):
            matrix[-1].append(byte & 1)
            byte >>= 1

regions = set()
seen = set()
q = []
for y in range(len(matrix)):
    for x in range(len(matrix[y])):
        if matrix[y][x] and (x, y) not in seen:
            q = [((x, y), {(x, y)})]
            while q:
                (cx, cy), cur_region = q.pop()
                seen.add((cx, cy))
                for (ax, ay) in adjacents(cx, cy):
                    if (ax, ay) not in seen:
                        if matrix[ay][ax]:
                            q.append(((ax, ay), cur_region | {(ax, ay)}))
                        else:
                            seen.add((ax, ay))
            regions.add(frozenset(cur_region))

print(len(regions))
print(datetime.datetime.now() - begin_time)
