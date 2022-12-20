import datetime
import itertools

begin_time = datetime.datetime.now()

paper = 0
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        dims = sorted(map(int, line.split('x')))
        paper += sum([(x * y) * 2 for x, y in itertools.combinations(dims, 2)]) + (dims[0] * dims[1])

print(paper)
print(datetime.datetime.now() - begin_time)
