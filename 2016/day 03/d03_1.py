import datetime

begin_time = datetime.datetime.now()

valids = 0
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        srtd = list(sorted(map(int, line.split())))
        if srtd[0] + srtd[1] > srtd[2]:
            valids += 1

print(valids)
print(datetime.datetime.now() - begin_time)
