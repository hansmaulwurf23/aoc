import datetime

begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    line = f.readlines()[0].rstrip()
    line = list(line)
    line.append(line[0])
    last_c = None
    sum = 0
    for c in line:
        if last_c is not None and c == last_c:
            sum += int(c)
        last_c = c
    print(sum)
print(datetime.datetime.now() - begin_time)
