import datetime

from knot_hash import knot_hash, knot_hash_hex, hex_hash

begin_time = datetime.datetime.now()

input = 'ljoxqyyw'
# input = 'flqrgnkx'
used = 0
for i in range(128):
    row_hash = knot_hash(f'{input}-{i}')
    while row_hash:
        byte = row_hash.pop()
        while byte:
            used += (byte & 1)
            byte >>= 1

print(used)
print(datetime.datetime.now() - begin_time)
