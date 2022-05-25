import datetime
import hashlib
import re

begin_time = datetime.datetime.now()

id = 'reyedfim'
# id = 'abc'
i = 0
pwd = [None] * 8
while True:
    if (h := hashlib.md5((id + str(i)).encode()).hexdigest())[0:5] == '00000':
        if re.match(r'\d', h[5]):
            idx = int(h[5])
            if idx < 8 and pwd[idx] is None:
                print(pwd)
                pwd[idx] = h[6]

    if all(pwd):
        print(''.join(pwd))
        break

    i += 1

print(datetime.datetime.now() - begin_time)
