import datetime
begin_time = datetime.datetime.now()

sum = 0
sums = set()
changes = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        changes.append(int(line))

i = 0
double = None
while True:
    for c in changes:
        sum += c
        if sum in sums:
            double = sum
            break
        else:
            sums.add(sum)

    if double is not None:
        print(double)
        break

print(datetime.datetime.now() - begin_time)
