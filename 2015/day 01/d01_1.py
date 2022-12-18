import datetime

begin_time = datetime.datetime.now()

print(sum(map(lambda c: 1 if c == '(' else -1, open('./input.txt').readline())))

print(datetime.datetime.now() - begin_time)
