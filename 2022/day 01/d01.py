import datetime

begin_time = datetime.datetime.now()
cals = []

with open('./input.txt') as f:
    cur_cal = 0
    for line in f.readlines():
        if line.rstrip():
            cur_cal += int(line)
        else:
            cals.append(cur_cal)
            cur_cal = 0

top_three = sorted(cals, reverse=True)[:3]
print(f'part 1: {top_three[0]}')
print(f'part 2: {sum(top_three)}')
print(datetime.datetime.now() - begin_time)
