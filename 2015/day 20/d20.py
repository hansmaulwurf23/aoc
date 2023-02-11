import datetime
from aopython import divisors

begin_time = datetime.datetime.now()

presents = 33100000
p = presents // 10
# this was just guessed
n = 700000
#n = 1
while True:
    divs = divisors(n)
    s = sum(divs)
    if s >= p:
        print(f'part 1: {n}')
        break
    n += 1

while True:
    divs = divisors(n)
    s50 = sum([d for d in divs if n // d <= 50]) * 11
    if s50 >= presents:
        print(f'part 2: {n}')
        break
    n += 1

print(datetime.datetime.now() - begin_time)
