import datetime

begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    sum = 0
    while line := f.readline().rstrip():
        numbers = list(map(int, line.split('\t')))
        sum += (max(numbers) - min(numbers))

print(sum)
print(datetime.datetime.now() - begin_time)
