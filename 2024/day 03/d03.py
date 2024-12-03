import datetime
import re

begin_time = datetime.datetime.now()

p1, p2 = 0, 0
enabled = True
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        while line:
            res = re.search(r'mul\(\d+,\d+\)|do\(\)|don\'t\(\)', line)
            if res:
                line = line[res.span()[1]:]
                m = res.group(0)
                if m == 'do()':
                    enabled = True
                elif m == "don't()":
                    enabled = False
                else:
                    a, b = list(map(int, m.replace('mul(', '').replace(')', '').split(',')))
                    p1 += (a * b)
                    p2 = p2 + (a * b) if enabled else p2
            else:
                break

print(f'part 1: {p1}')
print(f'part 2: {p2}')
print(datetime.datetime.now() - begin_time)
