import datetime

begin_time = datetime.datetime.now()

enhancements = dict()
image = ['.#.', '..#', '###']
steps = 18
cache = dict()

img_variants = [
    lambda i: list(i),
    lambda i: rotate(i),
    lambda i: rotate(rotate(i)),
    lambda i: rotate(rotate(rotate(i))),
    lambda i: flip(i),
    lambda i: flip(rotate(i)),
    lambda i: flip(rotate(rotate(i))),
    lambda i: rotate(flip(i))
]

with open('./input.txt') as f:
    while line := f.readline().rstrip():
        src, trgt = line.split(' => ')
        enhancements[tuple(src.split('/'))] = trgt.split('/')


def print_img(i):
    print('\n'.join(map(lambda r: ''.join(r), i)))
    print('')


def rotate(m):
    return list(map(lambda x: ''.join(x), [[m[j][i] for j in range(len(m))] for i in range(len(m[0]) - 1, -1, -1)]))


def flip(m):
    return [m[row] for row in range(len(m) - 1, -1, -1)]


def find_enhancement(tile):
    tile_size = len(tile[0])
    if tuple(tile) in cache:
        return cache[tuple(tile)]
    for pattern in filter(lambda x: len(x[0]) == tile_size, enhancements):
        for variant in img_variants:
            if variant(pattern) == tile:
                cache[tuple(tile)] = enhancements[pattern]
                return enhancements[pattern]


def split_tiles(img):
    tiles = []
    tile_size = 2 if len(img[0]) % 2 == 0 else 3
    tile_count = len(img) // tile_size
    for y in range(0, tile_count):
        tiles.append([])
        for x in range(0, tile_count):
            tiles[-1].append([])
            for tile_line in range(tile_size):
                tiles[-1][-1].append(img[(y * tile_size) + tile_line][(x * tile_size):((x + 1) * tile_size)])

    return tiles


def merge_tiles(tiles):
    ts = len(tiles[0][0])
    sz = len(tiles) * ts
    new_img = [None] * sz
    for y in range(sz):
        new_img[y] = [None] * sz
        for x in range(sz):
            new_img[y][x] = tiles[y // ts][x // ts][y % ts][x % ts]

    # merge cols
    for y, row in enumerate(new_img):
        new_img[y] = ''.join(new_img[y])
    return new_img


def count_lit_pixels(img):
    return sum(map(lambda row: row.count('#'), img))


for cycle in range(steps):
    tiles = split_tiles(image)
    print(cycle)
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            tiles[y][x] = find_enhancement(tile)
    image = merge_tiles(tiles)

print(count_lit_pixels(image))
print(datetime.datetime.now() - begin_time)
