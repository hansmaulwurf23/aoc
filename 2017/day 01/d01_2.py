import datetime

begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    line = list(f.readlines()[0].rstrip())
    print(sum([int(c)*2 for c, d in zip(line[:len(line) // 2], line[len(line) // 2:]) if c == d]))

print(datetime.datetime.now() - begin_time)
