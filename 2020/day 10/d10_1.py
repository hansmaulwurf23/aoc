import datetime

begin_time = datetime.datetime.now()
adapters = []

with open('./input.txt') as file:
    while line := file.readline().rstrip():
        adapters.append(int(line))

lastVal = 0
counters = [0, 0, 1]
for n in sorted(adapters):
    # print(f'{lastVal} {n}')
    counters[(n-lastVal)-1] += 1
    lastVal = n


print(counters)
print(counters[0] * counters[2])
print(datetime.datetime.now() - begin_time)
