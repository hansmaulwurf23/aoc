import datetime
from collections import defaultdict

begin_time = datetime.datetime.now()

distances = defaultdict(dict)
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        start, rest = line.split(' to ')
        end, dist = rest.split(' = ')
        distances[start][end] = int(dist)
        distances[end][start] = int(dist)

def find_optimum_distance(f, location, locations_left):
    global distances

    if not locations_left:
        return 0
    else:
        return f([distances[location][other] + find_optimum_distance(f, other, locations_left - {other}) for other in locations_left])


print(min([find_optimum_distance(min, l, distances.keys() - {l}) for l in distances.keys()]))
print(max([find_optimum_distance(max, l, distances.keys() - {l}) for l in distances.keys()]))
print(datetime.datetime.now() - begin_time)
