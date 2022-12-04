import datetime

begin_time = datetime.datetime.now()

overlap_counter = 0
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        s1, e1, s2, e2 = list(map(int, line.replace('-', ',').split(',')))
        if (s1 <= s2 <= e1) or (s2 <= s1 <= e2):
            overlap_counter += 1

print(overlap_counter)
print(datetime.datetime.now() - begin_time)
