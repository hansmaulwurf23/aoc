import datetime
from aopython import manhattan_distance

begin_time = datetime.datetime.now()

master = set()

moving = {
    'U': [0, 1],
    'D': [0, -1],
    'R': [1, 0],
    'L': [-1, 0]
}


def read_master(line):
    x, y = [0, 0]
    coords = set()
    for m in line.split(','):
        dir, steps = m[0], int(m[1:])
        xf, yf = moving[dir]
        for i in range(1, steps + 1):
            coords.add((x + (xf * i), y + (yf * i)))

        x, y = [x + (xf * steps), y + (yf * steps)]

    return coords


def find_cross_points(line, coords):
    x, y = [0, 0]
    cross_points = []
    for m in line.split(','):
        dir, steps = m[0], int(m[1:])
        xf, yf = moving[dir]
        for i in range(1, steps + 1):
            if (x + (xf * i), y + (yf * i)) in coords:
                cross_points.append((x + (xf * i), y + (yf * i)))

        x, y = [x + (xf * steps), y + (yf * steps)]

    return cross_points


with open('./input.txt') as f:
    lines = f.readlines()
    master = read_master(lines[0])
    cross_points = find_cross_points(lines[1], master)


print(cross_points)
distances = list(map(manhattan_distance, cross_points))
print(distances)
print(min(distances))
print(datetime.datetime.now() - begin_time)
