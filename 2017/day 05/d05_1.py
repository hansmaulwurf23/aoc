import datetime

begin_time = datetime.datetime.now()


def process(jumps):
    cur_idx = 0
    steps = 0
    while 0 <= cur_idx < len(jumps):
        steps += 1
        next_idx = jumps[cur_idx] + cur_idx
        jumps[cur_idx] += 1
        cur_idx = next_idx

    return steps

jumps = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        jumps.append(int(line))

print(process(jumps))
print(datetime.datetime.now() - begin_time)
