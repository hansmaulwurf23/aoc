import datetime

begin_time = datetime.datetime.now()

contain_counter = 0
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        s1, e1, s2, e2 = list(map(int, line.replace('-', ',').split(',')))
        if (s2 >= s1 and e2 <= e1) or (s1 >= s2 and e1 <= e2):
            contain_counter += 1

print(contain_counter)
print(datetime.datetime.now() - begin_time)
