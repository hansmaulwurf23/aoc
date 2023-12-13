import datetime
from collections import deque

begin_time = datetime.datetime.now()

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

# def is_valid(pattern: str, grouping: tuple):
#     grp = [0]
#     for i, c in enumerate(pattern):
#         if c == '.':
#             if grp[-1]:
#                 grp.append(0)
#         elif c == '#':
#             grp[-1] += 1
#
#     if grp[-1] == 0:
#         grp.pop()
#
#     return tuple(grp) == grouping


assert True == is_valid('##.##.#.#', (2, 2, 1, 1))
assert False == is_valid('##.##.#.#', (2, 1, 1, 1))
assert True == is_valid('#.#.###', (1, 1, 3))
assert True == is_valid('.#...#....###.', (1, 1, 3))
assert True == is_valid('.#.###.#.######', (1, 3, 1, 6))
assert True == is_valid('####.#...#...', (4, 1, 1))
assert True == is_valid('#....######..#####.', (1, 6, 5))
assert True == is_valid('.###.##....#', (3, 2, 1))
assert False == is_valid('.###.##.#.##', (3, 2, 1))
assert False == is_valid('.###......##', (3, 2, 1))

def arrangements(pattern: str, groupings):
    if '?' in pattern:
        if is_valid(pattern, groupings) == False:
            return set()
        return (arrangements(pattern.replace('?', '#', 1), groupings) |
                arrangements(pattern.replace('?', '.', 1), groupings))
    else:
        if is_valid(pattern, groupings):
            return {pattern}
        else:
            return set()


infos = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        springs, group_counts = line.split()
        infos.append([springs, tuple(map(int, group_counts.split(',')))])

counter = 0
for springs, group_count in infos:
    arrs = arrangements(springs, group_count)
    # print(springs, group_count, len(arrs), arrs)
    counter += len(arrs)

print(counter)
assert counter in [21, 7922]
print(datetime.datetime.now() - begin_time)
