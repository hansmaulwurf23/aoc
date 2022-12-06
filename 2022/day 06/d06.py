import datetime

begin_time = datetime.datetime.now()


def find_start(line, distinct_length=4):
    for i in range(len(line) - distinct_length):
        if len(set(line[i:i + distinct_length])) == distinct_length:
            return i + distinct_length


with open('./input.txt') as f:
    line = f.readline().rstrip()
    print(find_start(line, 4))
    print(find_start(line, 14))

print(datetime.datetime.now() - begin_time)
