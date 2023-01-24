import datetime
from collections import deque

begin_time = datetime.datetime.now()


def look_and_say(s):
    result = deque()
    i = 0
    c = 0
    last = None
    while i < (length := len(s)):
        if last != s[i]:
            if last is not None:
                result.append(f'{c}{last}')
            c = 1
            last = s[i]
        else:
            c += 1
        i += 1
    result.append(f'{c}{last}')

    return ''.join(result)

input = '1321131112'

for i in range(40):
    input = look_and_say(input)

print(f'part 1 {len(input)}')

for i in range(10):
    input = look_and_say(input)

print(f'part 2 {len(input)}')
print(datetime.datetime.now() - begin_time)
