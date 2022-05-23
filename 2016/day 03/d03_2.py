import datetime

begin_time = datetime.datetime.now()

valids = 0
vals = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        vals.append(list(map(int, line.split())))
        if len(vals) == 3:
            for i in range(3):
                srtd = list(sorted([x[i] for x in vals]))
                if srtd[0] + srtd[1] > srtd[2]:
                    valids += 1
            vals = []

print(valids)
print(datetime.datetime.now() - begin_time)
