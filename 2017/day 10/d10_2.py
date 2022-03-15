import datetime
from knot_hash import knot_hash_hex

begin_time = datetime.datetime.now()


with open('./input.txt') as f:
    print(knot_hash_hex(f.readlines()[0]))
print('decdf7d377879877173b7f2fb131cf1b')


print(knot_hash_hex(''))
print('a2582a3a0e66e6e86e3812dcb672a272')
print(knot_hash_hex('AoC 2017'))
print('33efeb34ea91902bb2f59c9920caa6cd')
print(knot_hash_hex('1,2,3'))
print('3efbe78a8d82f29979031a4aa0b16a9d')
print(knot_hash_hex('1,2,4'))
print('63960835bcdc130f0b66d7ff4f6a5a8e')
print(datetime.datetime.now() - begin_time)
