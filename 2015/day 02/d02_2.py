import datetime
import itertools

begin_time = datetime.datetime.now()

ribbon = 0
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        dims = sorted(map(int, line.split('x')))
        ribbon += sum([l * 2 for l in dims[:2]]) + (dims[0] * dims[1] * dims[2])

print(ribbon)
print(datetime.datetime.now() - begin_time)
