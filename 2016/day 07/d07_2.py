import datetime

begin_time = datetime.datetime.now()

valids = 0
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        i = 0
        in_hyper = False
        non_hypers = set()
        in_hypers = set()
        while i < len(line) - 2:
            if line[i] == '[':
                in_hyper = True
            elif line[i] == ']':
                in_hyper = False
            elif line[i] == line[i + 2] and line[i] != line[i + 1]:
                if in_hyper:
                    in_hypers.add(''.join([line[i+1], line[i], line[i+1]]))
                else:
                    non_hypers.add(line[i:i+3])

                if in_hypers & non_hypers:
                    print((in_hypers & non_hypers), line)
                    valids += 1
                    break
            i += 1

print(valids)
print(datetime.datetime.now() - begin_time)
