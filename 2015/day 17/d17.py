import datetime

begin_time = datetime.datetime.now()

eggnog = 150
containers = tuple(map(int, open('./input.txt', mode='r').readlines()))
# eggnog = 25
# containers = tuple([20, 15, 10, 5, 5])

min_len, min_count = len(containers), 0


def count_poss(eggnog, used, left):
    global min_len, min_count
    used_sum = sum(used)
    if used_sum > eggnog:
        return 0
    elif used_sum == eggnog:
        if len(used) < min_len:
            min_len = len(used)
            min_count = 1
        elif len(used) == min_len:
            min_count +=1
        return 1
    else:
        return sum([count_poss(eggnog, used + [l], left[i+1:]) for i, l in enumerate(left)])


print(f'part 1: {count_poss(eggnog, [], list(containers))}')
print(f'part 2: {min_count}')
print(datetime.datetime.now() - begin_time)
