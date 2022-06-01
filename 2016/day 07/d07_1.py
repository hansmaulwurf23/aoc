import datetime

begin_time = datetime.datetime.now()

valids = 0
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        i = 0
        in_hyper = False
        found = False
        while i < len(line) - 3:
            if line[i] == '[':
                in_hyper = True
            elif line[i] == ']':
                in_hyper = False
            elif line[i] == line[i + 3] and line[i + 1] == line[i + 2] and line[i] != line[i + 1]:
                # print(f'{line[0:i]}__{line[i:i+4]}__{line[i+4:]} ({valids})')
                if in_hyper:
                    break
                else:
                    found = True
            i += 1

        if i == len(line) - 3 and found:
            valids += 1

print(valids)
print(datetime.datetime.now() - begin_time)
