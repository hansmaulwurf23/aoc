import re
import datetime
begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    line = list(f.readlines()[0].rstrip())

output = []
ascii_diff = ord('a') - ord('A')
while len(line):
    output.append(line.pop(0))
    while len(output) and len(line) and abs(ord(output[-1]) - ord(line[0])) == ascii_diff:
        output.pop()
        line.pop(0)

print(len(output))
print(datetime.datetime.now() - begin_time)
