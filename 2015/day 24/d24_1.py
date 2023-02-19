import datetime
import functools
import itertools

begin_time = datetime.datetime.now()


# creates a list with all elements of all not in part (assumes both lists are ordered!)
def rest_list(all, part):
    rest, a = [], 0
    for p in part:
        while all[a] != p:
            rest.append(all[a])
            a += 1
        a += 1

    rest.extend(all[a:])

    return rest


def lower_bound(all, min_sum):
    lb, s = 1, all[0]
    while s < min_sum:
        s += all[lb]
        lb += 1
    return lb


nums = []
with open('./input.txt') as f:
    nums = list(sorted(map(int, f.readlines()), reverse=True))

# groups must have equal sums
grp_sum = sum(nums) // 3

# lower bound, upper bound for the number of elements in group 1
lb, ub, s = lower_bound(nums, grp_sum), len(nums) // 3, nums[0]

min_qe = None
for l in range(lb, ub + 1):
    for grp1 in (x for x in itertools.combinations(nums, l) if sum(x) == grp_sum):
        qe = functools.reduce(lambda a, b: a * b, grp1)
        if min_qe is not None and min_qe <= qe:
            continue
        rest = rest_list(nums, grp1)
        olb, oub, s = lower_bound(rest, grp_sum), len(rest) // 2, rest[0]

        for ol in range(olb, oub+1):
            if any((x for x in itertools.combinations(rest, ol) if sum(x) == grp_sum)):
                min_qe = qe
                break

    if min_qe is not None:
        break

print(min_qe)
print(datetime.datetime.now() - begin_time)
