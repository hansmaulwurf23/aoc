import datetime
import re
from aopython import manhattan_distance

begin_time = datetime.datetime.now()

max_r, file = 4000000, './input.txt'
# max_r, file = 20, './example.txt'
sensors = []


def find_lonesome_point():
    last_overlap = [None, None]
    for sensor, srange in sensors:
        sx, sy = sensor
        for x in range(max(0, sx - srange - 1), min(max_r + 1, sx + srange + 2)):
            # distance from edge of manhattan diamond to current x
            edge_distance = abs(x - sx)
            y_offset = (srange + 1 - edge_distance)
            # two points musts be examined (upper and lower) on the outside of the sensor diamond range
            points = [sy + y_offset, sy - y_offset]
            for i, y in enumerate(points):
                if 0 <= y <= max_r:
                    if last_overlap[i] is not None and manhattan_distance((x, y), last_overlap[i][0]) <= last_overlap[i][1]:
                        break
                    for other_sensor, other_range in sensors:
                        if manhattan_distance((x, y), other_sensor) <= other_range:
                            # store last overlapping sensor provides six times faster runtime
                            last_overlap[i] = (other_sensor, other_range)
                            break
                    else:
                        return x, y


with open(file) as f:
    while line := f.readline().rstrip():
        sx, sy, bx, by = list(map(int, re.findall(r'(-?\d+)', line)))
        sensor, beacon = tuple([sx, sy]), tuple([bx, by])
        mh = manhattan_distance(sensor, beacon)
        sensors.append((sensor, mh))
    sensors = list(sorted(sensors, key=lambda x: x[0][1]))

# this runs for 2 hours :(
# for y in range(max_r):
#     xranges = []
#     for sensor, mh in sensors:
#         sx = sensor[0]
#         perpendicular = tuple([sx, y])
#         perp_mh = manhattan_distance(sensor, perpendicular)
#         # sensor within range of line
#         if mh >= perp_mh:
#             d = mh - perp_mh
#             srange = range(max(sx - d, 0), min(sx + d, max_r) + 1)
#             merged = False
#             for i, xr in enumerate(xranges):
#                 if range_in_range(srange, xr):
#                     # range completely within another range
#                     merged = True
#                     break
#                 elif range_in_range(xr, srange):
#                     merged = True
#                     xranges[i] = srange
#                 elif srange.start in xr:
#                     merged = True
#                     xranges[i] = range(xr.start, max(srange.stop, xr.stop))
#                 elif srange.stop in xr:
#                     merged = True
#                     xranges[i] = range(srange.start, max(srange.stop, xr.stop))
#
#                 if merged and i < len(xranges) - 1:
#                     if xranges[i].stop in xranges[i+1]:
#                         xranges[i] = range(xranges[i].start, xranges[i+1].stop)
#                         xranges.remove(xranges[i+1])
#                     elif xranges[i].stop >= xranges[i+1].stop:
#                         xranges[i] = range(xranges[i].start, xranges[i].stop)
#                         xranges.remove(xranges[i+1])
#
#             # no more possible x?
#             if len(xranges) == 1 and xranges[0] == range(0, max_r + 1):
#                 break
#
#             # still have to add srange?
#             if not merged:
#                 xranges.append(srange)
#                 xranges = sorted(xranges, key=lambda s: s.start)
#
#     #if len(xranges) > 1:
#     #print(y, xranges)
#     if len(xranges) == 2:
#         print(f'{xranges[0].stop * max_r + y} {y} {xranges[0].stop}')
#         break

px, py = find_lonesome_point()
print(f'{px * max_r + py}')
print('12525726647448')
print(datetime.datetime.now() - begin_time)
