import datetime
import re
begin_time = datetime.datetime.now()

p1re = re.compile(r'^(\d+)\1$')
p2re = re.compile(r'^(\d+)\1+$')
part1, part2 = 0, 0
with open('./input.txt') as f:
    for start, end in [list(map(int, e.split('-'))) for e in f.readline().rstrip().split(',')]:
        for i in range(start, end + 1):
            if p1re.match(str(i)):
                part1 += i
                part2 += i
            elif p2re.match(str(i)):
                part2 += i


print(f'part 1: {part1}')
print(f'part 2: {part2}')
assert part1 in (29818212493, 1227775554)
assert part2 in (37432260594, 4174379265)

print(datetime.datetime.now() - begin_time)
