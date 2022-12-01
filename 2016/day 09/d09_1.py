import datetime
import re
begin_time = datetime.datetime.now()


def decode(line):
    result = []
    i = 0
    while i < len(line):
        if line[i] == '(':
            rep = re.findall(r'\(\d+x\d+\)', line[i:])[0]
            i += len(rep)
            chrs, repeat = list(map(int, rep[1:-1].split('x')))
            for r in range(repeat):
                result.append(line[i:i+chrs])
            i += chrs
        else:
            result.append(line[i])
            i += 1

    return ''.join(result)


sum_size = 0
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        sum_size += len(decode(line))

print(sum_size)
print(datetime.datetime.now() - begin_time)
