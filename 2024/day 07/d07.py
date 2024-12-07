import datetime
from collections import deque

begin_time = datetime.datetime.now()


def dfs(val, res, ops, idx, use_concat = False):
    if idx == len(ops):
        return 1 if val == res else 0

    if res > val:
        return 0

    nxt_op = ops[idx]
    if res == 0:
        return dfs(val, nxt_op, ops, idx+1, use_concat)
    else:
        return 0 \
            + (dfs(val, int(str(res) + str(nxt_op)), ops, idx+1, use_concat) if use_concat else 0) \
            + dfs(val, res * nxt_op, ops, idx+1, use_concat) \
            + dfs(val, res + nxt_op, ops, idx+1, use_concat) \
            + 0


sum1, sum2 = 0, 0
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        test_val, obs = line.split(': ')
        test_val, obs = int(test_val), list(map(int, obs.split(' ')))
        cnt = dfs(test_val, 0, obs, 0)
        sum1 += (test_val if cnt else 0)
        if not cnt:
            cnt = dfs(test_val, 0, obs, 0, use_concat = True)
        sum2 += (test_val if cnt else 0)

assert sum1 in (1545311493300, 3749)
assert sum2 in (169122112716571, 11387)
print(f'part 1: {sum1}')
print(f'part 2: {sum2}')
print(datetime.datetime.now() - begin_time)
