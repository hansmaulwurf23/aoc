import datetime
import re
begin_time = datetime.datetime.now()

dir_deltas = {
    'e': (2, 0),
    'ne': (1, 1),
    'se': (1, -1),
    'w': (-2, 0),
    'nw': (-1, 1),
    'sw': (-1, -1),
}
flipped_tiles = set()


def follow_path(line):
    x, y = [0, 0]
    while line:
        curDir = re.match(r'^(e|w|sw|se|nw|ne)', line).group(0)
        dx, dy = dir_deltas[curDir]
        (x, y) = (x + dx, y + dy)
        line = line[len(curDir):]

    if (x, y) in flipped_tiles:
        # print(f'flipping ({x},{y}) back to white')
        flipped_tiles.remove((x, y))
    else:
        # print(f'flipping ({x},{y}) to black')
        flipped_tiles.add((x, y))


with open('./input.txt') as file:
    while line := file.readline().rstrip():
        follow_path(line)

print(len(flipped_tiles))
print(datetime.datetime.now() - begin_time)
