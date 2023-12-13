import datetime
from collections import deque
from functools import cache
from itertools import permutations, product

begin_time = datetime.datetime.now()


def fold(pattern, n: int):
    return '?'.join([pattern] * n)

def tokenize(pattern: str):
    return list(filter(lambda l: l, pattern.split('.')))

def min_max_counts(tok_list: list):
    return [deque([e.count('#') for e in tok_list]),
            deque([len(e) for e in tok_list])]

def is_valid(pattern: str, grouping):
    t = deque(grouping)
    gl = 0
    for i, c in enumerate(pattern):
        if c == '.':
            if gl:
                if not t or t[0] != gl:
                    return False
                else:
                    gl = 0
                    t.popleft()
        elif c == '#':
            gl += 1
        elif c == '?':
            return None

    return not gl if not t else t[0] == gl and len(t) == 1


@cache
def arrangements(remaining_springs, remaining_groups):
    cntr = 0
    # all remaining springs plus at least as many dots as groups are left minus all positions needed for springs
    first_group_max_len = len(remaining_springs) + len(remaining_groups) - sum(remaining_groups)
    # print(f'first_group_max_len = {first_group_max_len}, remaining {remaining_springs} {remaining_groups}')
    for front_len in range(first_group_max_len):
        first_group = f"{'.' * front_len}{'#' * remaining_groups[0]}."
        first_group_len = len(first_group)
        # print(first_group, front_len, remaining_groups)

        if all(spring == elem or spring == '?' for spring, elem in zip(remaining_springs, first_group)):
            if not remaining_groups[1:]:
                if '#' not in remaining_springs[first_group_len:]:
                    cntr += 1
            else:
                cntr += arrangements(remaining_springs[len(first_group):], remaining_groups[1:])

    return cntr


@cache
def pattern_permutations(pattern: str):
    @cache
    def perm(pattern: str):
        if '?' in pattern:
            return perm(pattern.replace('?', '.', 1)) + \
                   perm(pattern.replace('?', '#', 1))
        else:
            return [pattern]

    ps = perm(pattern)
    # print(ps)
    res = []
    for t in [tokenize(p) for p in ps]:
        res.append([x.count('#') for x in t])
    return res

def count_arrs(pattern: list, g):
    tokened_perms = [pattern_permutations(p) for p in pattern]

    def count(tokened, used, g):
        if len(used) > len(g):
            return 0

        if not tokened:
            return 1 if tuple(used) == g else 0

        return sum([count(tokened[1:], used + p, g) for p in tokened[0]])

    return count(tokened_perms, [], g)


infos = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        springs, group_counts = line.split()
        infos.append([springs, tuple(map(int, group_counts.split(',')))])

counter = 0
for springs, group_counts in infos:
    counter += arrangements('?'.join((springs,) * 5), group_counts * 5)

print(counter)
# print('11863964946257 too low')
print(datetime.datetime.now() - begin_time)
