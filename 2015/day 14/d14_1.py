import datetime
import re
from collections import defaultdict

begin_time = datetime.datetime.now()

racedeers = dict()
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        speed, endurance, pit = map(int, re.findall(r'\d+', line))
        name = line.split(' ', maxsplit=1)[0]
        racedeers[name] = tuple([speed, endurance, pit])

max_dist = 0
race_len = 2503
for name, (speed, endurance, pit) in racedeers.items():
    laps = race_len // (endurance + pit)
    dist = speed * laps * endurance
    dist += min(race_len - laps * (endurance + pit), endurance) * speed

    if dist > max_dist:
        max_dist = dist

print(max_dist)

distances, points = defaultdict(int), defaultdict(int)
for second in range(race_len):
    max_dist = 0
    for name, (speed, endurance, pit) in racedeers.items():
        if second % (endurance + pit) < endurance:
            distances[name] += speed
        if max_dist < distances[name]:
            max_dist = distances[name]

    for name in [name for name, dist in distances.items() if dist == max_dist]:
        points[name] += 1

print(max(points.values()))
print(datetime.datetime.now() - begin_time)
