import datetime

begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    nums = [int(l.rstrip()) for l in f.readlines()]

print(f'part 1: {sum([1 if a < b else 0 for a, b in zip(nums, nums[1:])])}')

s1, c = sum(nums[:3]), 0
for r, e in zip(nums, nums[3:]):
    s2 = s1 - r + e
    if s1 < s2:
        c += 1
    s1 = s2
print(f'part 2: {c}')
print(datetime.datetime.now() - begin_time)
