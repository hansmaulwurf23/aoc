import datetime
begin_time = datetime.datetime.now()

vesselLoc = [0, 0]
waypoint = [10, 1]

# https://en.wikipedia.org/wiki/Rotation_matrix#Common_rotations
cclockwiseRot = [
    lambda x, y: [x, y],
    lambda x, y: [-y, x],
    lambda x, y: [-x, -y],
    lambda x, y: [y, -x]
]

moving = {
    'N': lambda t: [0, t],
    'S': lambda t: [0, -t],
    'E': lambda t: [t, 0],
    'W': lambda t: [-t, 0]
}

with open('./input.txt') as file:
    while line := file.readline().rstrip():
        (cmd, amount) = [line[0], int(line[1:])]

        if cmd == 'F':
            vesselLoc = [vesselLoc[0] + (waypoint[0] * amount), vesselLoc[1] + (waypoint[1] * amount)]
        if cmd in moving.keys():
            (dx, dy) = moving[cmd](amount)
            waypoint = [waypoint[0] + dx, waypoint[1] + dy]
        if cmd == 'R':
            cmd = 'L'
            amount = 360 - amount
        if cmd == 'L':
            waypoint = cclockwiseRot[(amount//90)](*waypoint)

print(f'{abs(vesselLoc[0]) + abs(vesselLoc[1])}')
print(datetime.datetime.now() - begin_time)
