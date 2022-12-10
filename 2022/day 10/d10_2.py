import datetime

begin_time = datetime.datetime.now()

OPCYCLES = {'noop': 1, 'addx': 2}

X = 1
cycle = 0
crt = []
ROWS, PIXELS = 6, 40
for row in range(ROWS):
    crt.append([False] * PIXELS)

with open('./input.txt') as f:
    while line := f.readline().rstrip():
        cmd = line.split(' ')[0]
        for c in range(OPCYCLES[cmd]):
            row = cycle // PIXELS
            pixel = cycle % PIXELS
            if abs(pixel - X) <= 1:
                crt[row][pixel] = True
            cycle += 1

        if cmd == 'addx':
            X += int(line[4:])

for row in crt:
    print(' '.join(map(lambda x: '#' if x else '.', row)))

print(datetime.datetime.now() - begin_time)
