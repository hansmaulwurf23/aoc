import datetime
from itertools import pairwise
from aopython import cmp

begin_time = datetime.datetime.now()


def evaluate(nums):
    sign = cmp(nums[0], nums[1])
    return [True if cmp(a, b) == sign and 1 <= abs(a - b) <= 3 else False for a, b in pairwise(nums)]


def can_be_fixed(nums, evaluation):
    idx = evaluation.index(False)
    for offset in [-1, 0, 1]:
        test = nums[:idx + offset] + nums[idx + 1 + offset:]
        if all(evaluate(test)):
            return True
    return False


valid = 0
corrected = 0
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        nums = list(map(int, line.split()))
        evaluation = evaluate(nums)
        if all(evaluation):
            valid += 1
        elif can_be_fixed(nums, evaluation):
            corrected += 1

print(f'part 1: {valid}')
print(f'part 2: {valid + corrected}')
print(datetime.datetime.now() - begin_time)
