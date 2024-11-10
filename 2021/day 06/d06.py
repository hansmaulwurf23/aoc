import datetime
from functools import cache
from aopython import sign

begin_time = datetime.datetime.now()
BIRTH_CYCLE = 6
MATING_AGE = 8

@cache
def aging(rest, age):
    if rest < 0:
        return 1

    rest -= 1
    if age == BIRTH_CYCLE:
        return aging(rest, BIRTH_CYCLE - 1) + aging(rest, -(MATING_AGE - 1))

    return aging(rest, BIRTH_CYCLE if age == 0 else age - sign(age))


def mating_days(days):
    fishes = 0
    for age in ages:
        fishes += aging(days, age)
    return fishes

with open('./input.txt') as f:
    ages = list(map(int, f.readline().rstrip().split(',')))

print(f'part 1: {mating_days(80)}')
print(f'part 2: {mating_days(256)}')
print(datetime.datetime.now() - begin_time)
