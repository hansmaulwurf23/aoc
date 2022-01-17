import datetime
begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    print(sum([i//3 - 2 for i in map(int, f.readlines())]))

print(datetime.datetime.now() - begin_time)
