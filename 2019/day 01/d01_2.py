import datetime
begin_time = datetime.datetime.now()

def calc_fuel(weight):
    fuel = (weight // 3) - 2
    if fuel > 0:
        fuel += calc_fuel(fuel)
    elif fuel < 0:
        fuel = 0

    return fuel


with open('./input.txt') as f:
    modules = list(map(int, f.readlines()))


sum_fuel = 0
for m in modules:
    sum_fuel += calc_fuel(m)

print(sum_fuel)
print(datetime.datetime.now() - begin_time)
