import datetime
from aopython import last_digit, ceildiv

begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    numbers = list(map(int, f.readlines()[0].rstrip()))
    numbers = numbers

skip = int(''.join(list(map(str, numbers[0:7]))))
num_len = len(numbers)
target_len = num_len * 10000 - skip
numbers = numbers * ceildiv(target_len, num_len)
numbers = numbers[(len(numbers)-target_len):]
# note that skip needs to be greater than len(numbers) * 10000 for this to work!

for i in range(100):
    x = 0
    for n in range(target_len - 1, -1, -1):
        x += numbers[n]
        numbers[n] = last_digit(x)

print(numbers[0:8])
print(datetime.datetime.now() - begin_time)
