import datetime

begin_time = datetime.datetime.now()

val_sum = 0

with open('./input.txt') as f:
    while line := f.readline().rstrip():
        half_len = len(line) // 2
        c1, c2 = set(line[0:half_len]), set(line[half_len:])
        same = list(c1.intersection(c2))[0]
        if ord(same) >= ord('a'):
            v = ord(same) - ord('a') + 1
        else:
            v = ord(same) - ord('A') + 27

        val_sum += v

print(val_sum)
print(datetime.datetime.now() - begin_time)
