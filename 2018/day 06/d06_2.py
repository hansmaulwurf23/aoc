import datetime
import showgrid
from aopython import min_max_2d, manhattan_distance
begin_time = datetime.datetime.now()

tt_max = 10000

def process(locations):
    fx, tx, fy, ty = min_max_2d(locations)
    ttclub = set()
    for x, y in [(x, y) for x in range(fx, tx + 1) for y in range(fy, ty + 1)]:
        cur_sum = 0
        for l in locations:
            cur_sum += manhattan_distance(l, (x, y))
            if cur_sum > tt_max:
                break

        if cur_sum < tt_max:
            ttclub.add((x, y))

    return ttclub

locations = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        locations.append(tuple(map(int, line.split(', '))))

tittie_club = process(locations)
showgrid.show_grid(tittie_club, highlights=locations, s=10)
print(len(tittie_club))
print(datetime.datetime.now() - begin_time)
