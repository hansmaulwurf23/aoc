import datetime
import re

begin_time = datetime.datetime.now()

s = 0
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        s += sum(map(int, re.findall(r'-?\d+', line)))

print(s)
print(datetime.datetime.now() - begin_time)
