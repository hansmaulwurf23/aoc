import datetime
from functools import cache

begin_time = datetime.datetime.now()


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
