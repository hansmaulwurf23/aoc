import datetime
begin_time = datetime.datetime.now()

vesselLoc = [0, 0]
vesselDir = [1, 0]

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
            (dx, dy) = [vesselDir[0] * amount, vesselDir[1] * amount]
        if cmd in moving.keys():
            (dx, dy) = moving[cmd](amount)
        if cmd == 'R':
            cmd = 'L'
            amount = 360 - amount
        if cmd == 'L':
            vesselDir = cclockwiseRot[(amount//90)](*vesselDir)
            (dx, dy) = (0, 0)

        vesselLoc = [vesselLoc[0] + dx, vesselLoc[1] + dy]

print(f'{abs(vesselLoc[0]) + abs(vesselLoc[1])}')
print(datetime.datetime.now() - begin_time)
