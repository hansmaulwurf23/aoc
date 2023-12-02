import datetime
begin_time = datetime.datetime.now()

print(sum(list(map(lambda l: 10 * l[0] + l[-1], map(lambda l: list(map(int, filter(lambda c: '0' <= c <= '9', l))), open('./input.txt'))))))

print(datetime.datetime.now() - begin_time)
