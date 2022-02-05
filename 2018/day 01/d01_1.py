import datetime
begin_time = datetime.datetime.now()

sum = 0
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        sum += int(line)

print(sum)
print(datetime.datetime.now() - begin_time)
