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
grp_sum = sum(nums) // 4

min_qe = None
for len1 in range(lower_bound(nums, grp_sum), len(nums) // 4 + 1):
    for grp1 in (x for x in itertools.combinations(nums, len1) if sum(x) == grp_sum):
        qe = functools.reduce(lambda a, b: a * b, grp1)
        if min_qe is not None and min_qe <= qe:
            continue

        rest1 = rest_list(nums, grp1)
        for grp2 in ((x for x in itertools.combinations(rest1, len2) if sum(x) == grp_sum)
                     for len2 in range(lower_bound(rest1, grp_sum), len(rest1) // 3 + 1)):
            rest2 = rest_list(rest1, grp2)
            if any(((x for x in itertools.combinations(rest2, len3) if sum(x) == grp_sum)
                    for len3 in range(lower_bound(rest2, grp_sum), len(rest2) // 2 + 1))):
                min_qe = qe
                found = True
                break

    if min_qe is not None:
        break

print(min_qe)
print(datetime.datetime.now() - begin_time)
