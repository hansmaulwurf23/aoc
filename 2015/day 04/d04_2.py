import datetime
import hashlib

begin_time = datetime.datetime.now()

prefix = 'bgvyzdsv'
i = 0
while True:
    he = hashlib.md5(f'{prefix}{i}'.encode()).hexdigest()
    if str(he).startswith('000000'):
        print(i)
        break
    else:
        i += 1

print(datetime.datetime.now() - begin_time)
