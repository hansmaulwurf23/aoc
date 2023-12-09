import datetime
from collections import defaultdict
begin_time = datetime.datetime.now()

counts = defaultdict(int)
nums = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        nums.append(line)
        for i, c in enumerate(line):
            counts[i] += 1 if c == '1' else -1


def binstr_to_int(s):
    v = 0
    for d in s:
        v = (v << 1) + int(d)
    return v


def part1(counts):
    gamma = 0
    for k in sorted(counts.keys()):
        gamma = (gamma << 1) + (1 if counts[k] > 0 else 0)

    xor_pattern = (1 << max(counts) + 1) - 1
    epsilon = xor_pattern ^ gamma
    print(f'part1: {gamma * epsilon}')


def retain(l, idx, return_least=False):
    if len(l) == 1:
        return l

    ones, zeros = [], []
    for e in l:
        if e[idx] == '1':
            ones.append(e)
        else:
            zeros.append(e)

    if len(zeros) > len(ones):
        most, least = zeros, ones
    elif len(zeros) < len(ones):
        most, least = ones, zeros
    else:
        if return_least:
            return zeros
        else:
            return ones

    return least if return_least else most


def part2(nums):
    l = len(nums[0])
    oxy, cdo = nums, nums
    for i in range(l):
        oxy = retain(oxy, i, False)
        cdo = retain(cdo, i, True)

    oxy = binstr_to_int(oxy[0])
    cdo = binstr_to_int(cdo[0])
    print(f'part2: {oxy * cdo}')


part1(counts)
part2(nums)
print(datetime.datetime.now() - begin_time)
