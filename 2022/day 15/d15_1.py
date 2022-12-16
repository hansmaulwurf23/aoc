import datetime
import re
from aopython import manhattan_distance

begin_time = datetime.datetime.now()

# inspect_line = 10
inspect_line = 2000000
min_line_x, max_line_x = None, None

with open('./input.txt') as f:
    while line := f.readline().rstrip():
        sx, sy, bx, by = list(map(int, re.findall(r'(-?\d+)', line)))
        sensor, beacon = tuple([sx, sy]), tuple([bx, by])
        perpendicular = tuple([sx, inspect_line])
        mh = manhattan_distance(sensor, beacon)
        perp_mh = manhattan_distance(sensor, perpendicular)
        # sensor within range of line
        if mh >= perp_mh:
            #print(f'sensor {sensor} (mh to beacon {mh}, mh to perpendicular {perp_mh} within range of y={inspect_line}')
            d = mh - perp_mh
            my_min_x = sx - d
            my_max_x = sx + d
            if min_line_x is None or min_line_x > my_min_x:
                min_line_x = my_min_x
            if max_line_x is None or max_line_x < my_max_x:
                max_line_x = my_max_x


print(max_line_x - min_line_x)
print(datetime.datetime.now() - begin_time)
