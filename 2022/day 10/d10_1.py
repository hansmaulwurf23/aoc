import datetime

begin_time = datetime.datetime.now()

OPCYCLES = {'noop': 1, 'addx': 2}

X = 1
cycle = 0
signal_strengths = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        cmd = line.split(' ')[0]
        for c in range(OPCYCLES[cmd]):
            cycle += 1
            if cycle % 40 == 20:
                signal_strengths.append(cycle * X)

        if cmd == 'addx':
            X += int(line[4:])

print(sum(signal_strengths))
print(datetime.datetime.now() - begin_time)
