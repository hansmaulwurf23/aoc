import datetime
from collections import defaultdict

begin_time = datetime.datetime.now()

compat = defaultdict(dict)
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        splits = line.split(' ')
        name = splits[0]
        val = int(splits[3]) if splits[2] == 'gain' else -int(splits[3])
        neighbor = splits[-1][:-1]
        compat[name][neighbor] = val


def make_seating(name, rest):
    global compat

    if not rest:
        return compat[name]['Bob'] + compat['Bob'][name]
    else:
        return max([compat[name][other] + compat[other][name] + make_seating(other, rest - {other}) for other in rest])


print(make_seating('Bob', compat.keys() - {'Bob'}))

for k in compat.keys():
    compat[k]['Yourself'] = 0

compat['Yourself'] = dict()
for k in compat.keys():
    compat['Yourself'][k] = 0

print(make_seating('Bob', compat.keys() - {'Bob'}))
print(datetime.datetime.now() - begin_time)
