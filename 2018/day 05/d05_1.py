import re
import datetime
begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    line = f.readlines()[0].rstrip()

regex = '('
for l, u in zip(range(ord('a'), ord('z') + 1), range(ord('A'), ord('Z') + 1)):
        regex += f'{chr(l)}{chr(u)}|{chr(u)}{chr(l)}|'
regex += '__)+'

while newline := re.sub(regex, '', line):
    if newline == line:
        break
    else:
        # print(len(newline))
        line = newline
print(len(line))
print(datetime.datetime.now() - begin_time)
