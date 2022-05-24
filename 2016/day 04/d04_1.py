import datetime
import re
from collections import Counter

begin_time = datetime.datetime.now()

s = 0
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        name, id, chksm = re.match(r"([^0-9]+)(\d+)\[(.*)\]", line).groups()
        if ''.join(map(lambda x: x[0], Counter(sorted(name.replace('-', ''))).most_common(5))) == chksm:
            s += int(id)

print(s)
print(datetime.datetime.now() - begin_time)
