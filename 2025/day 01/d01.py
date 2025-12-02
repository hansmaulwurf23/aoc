import datetime

begin_time = datetime.datetime.now()

dial = 50
part1, part2 = 0, 0
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        dir, stps = line[0], int(line[1:])
        if dir == 'L':
            part2 += (1 if dial > 0 else 0) + (stps - dial) // 100 if stps >= dial else 0
            dial = (dial - stps) % 100
        else:
            part2 += (dial + stps) // 100
            dial = (dial + stps) % 100

        if dial == 0:
            part1 += 1

        # print(dir, stps, dial, part1, part2)

print(f'part 1: {part1}')
print(f'part 2: {part2}')
print(datetime.datetime.now() - begin_time)
