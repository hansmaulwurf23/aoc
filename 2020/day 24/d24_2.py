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
black_tiles = set()


def get_min_max(tiles):
    fx, tx, fy, ty = [None] * 4
    for t in tiles:
        if tx is None or t[0] > tx: tx = t[0]
        if fx is None or t[0] < fx: fx = t[0]
        if ty is None or t[1] > ty: ty = t[1]
        if fy is None or t[1] < fy: fy = t[1]

    return fx, tx, fy, ty


def follow_path(line):
    x, y = [0, 0]
    while line:
        curDir = re.match(r'^(e|w|sw|se|nw|ne)', line).group(0)
        dx, dy = dir_deltas[curDir]
        (x, y) = (x + dx, y + dy)
        line = line[len(curDir):]

    if (x, y) in black_tiles:
        # print(f'flipping ({x},{y}) back to white')
        black_tiles.remove((x, y))
    else:
        # print(f'flipping ({x},{y}) to black')
        black_tiles.add((x, y))


def run_day(black_tiles):
    new_black_tiles = set()
    fx, tx, fy, ty = get_min_max(black_tiles)
    for y in range(fy - 1, ty + 2):
        for x in range(fx - 2 - ((y + fx) % 2), tx + 2 + ((y + fx) % 2) + 1, 2):
            blacks = len([(ax, ay) for ax, ay in dir_deltas.values() if (ax + x, ay + y) in black_tiles])
            if (x, y) in black_tiles:
                if not (blacks == 0 or blacks > 2):
                    new_black_tiles.add((x, y))
            else:
                if blacks == 2:
                    new_black_tiles.add((x, y))

    return new_black_tiles


with open('./input.txt') as file:
    while line := file.readline().rstrip():
        follow_path(line)


for day in range(100):
    black_tiles = run_day(black_tiles)

print(len(black_tiles))
print(datetime.datetime.now() - begin_time)
