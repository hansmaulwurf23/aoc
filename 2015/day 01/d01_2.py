import datetime

begin_time = datetime.datetime.now()

instr = list(open('./input.txt').readline())
floor = 0
for i, c in enumerate(instr):
    floor += 1 if c == '(' else -1
    if floor == -1:
        print(i+1)
        break
print(datetime.datetime.now() - begin_time)
