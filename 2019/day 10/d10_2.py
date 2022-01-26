import datetime
import math

begin_time = datetime.datetime.now()
asteroids = []


def gcd(a, b):
    while b != 0:
        (a, b) = (b, a % b)
    return a


# turn direction into a clockwise angle: convert cartesian into polar coordinates but system is mirrored
# on x-axis (since up is actually down!) and polar coordinates start 90 degrees rotated on x-axis
def clock_angle(v):
    x, y = v[0], v[1]
    angle = math.degrees(math.atan2(y, x)) + 90
    if angle < 0:
        angle = 360 + angle
    return angle


def vec_add(a, b):
    return a[0] + b[0], a[1] + b[1]


def find_line_of_sights(asteroids):
    line_of_sights = dict()
    for a in asteroids:
        line_of_sights[a] = set()
        for o in [_ for _ in asteroids if _ != a]:
            # calc vector between asteroids a and o
            vector = [o[0] - a[0], o[1] - a[1]]
            # reduce the fraction (aka direction)
            divisor = gcd(abs(vector[0]), abs(vector[1]))
            vector = (vector[0] // divisor, vector[1] // divisor)
            # since value of dict is a set we don't store same line of sight twice
            line_of_sights[a].add(vector)

    return line_of_sights


with open('./input.txt') as f:
    y = 0
    while line := f.readline().rstrip():
        asteroids.extend([(x, y) for x, c in enumerate(line) if c == '#'])
        y += 1
asteroids = set(asteroids)

line_of_sights = find_line_of_sights(asteroids)
# best asteroid is the one with the most directions
besteroid = max(line_of_sights, key=(lambda k: len(line_of_sights[k])))
# since besteroid has 326 asteroids in line of sight, we don't even need a whole turn of the vapo-laser
# therefore its sufficient to find the 200th direction (converted into "clock angles")
clock_angles = {clock_angle(l): l for l in line_of_sights[besteroid]}
direction = clock_angles[sorted(clock_angles.keys())[199]]
# start on besteroid and move this direction until the first asteroid is found
loc = vec_add(besteroid, direction)
while loc not in asteroids:
    loc = vec_add(loc, direction)
# BOOM
print(loc[0] * 100 + loc[1])
print(datetime.datetime.now() - begin_time)
