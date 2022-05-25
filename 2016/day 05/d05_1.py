import datetime
import hashlib
begin_time = datetime.datetime.now()

id = 'reyedfim'
# id = 'abc'
i = 0
pwd = []
while True:
    if (h := hashlib.md5((id + str(i)).encode()).hexdigest())[0:5] == '00000':
        print(h[5])
        pwd.append(h[5])

    if len(pwd) == 8:
        print(''.join(pwd))
        break

    i += 1

print(datetime.datetime.now() - begin_time)
