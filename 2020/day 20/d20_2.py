import datetime
import re
from functools import reduce

begin_time = datetime.datetime.now()

(UP, DOWN, LEFT, RIGHT) = (0, 1, 2, 3)
tiles = dict()
edges = dict()
jigsaw = dict()
image = []


def print_tiles():
    for row in image:
        print(f'{"".join([c for c in row])}')


def edge_to_int(edge):
    return int(''.join(['1' if it == '#' else '0' for it in edge]), 2)


def flip_edge(edge):
    return int(''.join(reversed(list(f'{edge:010b}'))), 2)


def rotate_matrix(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0])-1, -1, -1)]


def vflip_matrix(m):
    return [m[row] for row in range(len(m) - 1, -1, -1)]


def hflip_matrix(m):
    return [list(reversed(m[row])) for row in range(len(m))]


def vflip_tile(tileNo):
    tiles[tileNo] = vflip_matrix(tiles[tileNo])
    jigsaw[tileNo] = [jigsaw[tileNo][DOWN], jigsaw[tileNo][UP], jigsaw[tileNo][LEFT], jigsaw[tileNo][RIGHT]]
    edges[tileNo] = store_edges(tiles[tileNo])


def hflip_tile(tileNo):
    tiles[tileNo] = hflip_matrix(tiles[tileNo])
    jigsaw[tileNo] = [jigsaw[tileNo][UP], jigsaw[tileNo][DOWN], jigsaw[tileNo][RIGHT], jigsaw[tileNo][LEFT]]
    edges[tileNo] = store_edges(tiles[tileNo])


def rotate_tile(tileNo):
    tiles[tileNo] = rotate_matrix(tiles[tileNo])
    jigsaw[tileNo] = [jigsaw[tileNo][RIGHT], jigsaw[tileNo][LEFT], jigsaw[tileNo][UP], jigsaw[tileNo][DOWN]]
    edges[tileNo] = store_edges(tiles[tileNo])


def store_edges(tile):
    result = [None] * 4
    result[UP] = edge_to_int(tile[0])
    result[DOWN] = edge_to_int(tile[-1])
    result[LEFT] = edge_to_int([it[0] for it in [row for row in tile]])
    result[RIGHT] = edge_to_int([it[-1] for it in [row for row in tile]])

    return result


def complete_jigsaw_row(leftEdgeTileNo):
    curTileNo = leftEdgeTileNo
    nextTileNo = jigsaw[curTileNo][RIGHT]
    while nextTileNo:
        while jigsaw[nextTileNo][LEFT] != curTileNo:
            rotate_tile(nextTileNo)
        if edges[curTileNo][RIGHT] != edges[nextTileNo][LEFT]:
            vflip_tile(nextTileNo)

        curTileNo = nextTileNo
        nextTileNo = jigsaw[nextTileNo][RIGHT]


def complete_jigsaw(topLeftTileNo):
    curTileNo = topLeftTileNo
    while True:
        complete_jigsaw_row(curTileNo)
        nextTileNo = jigsaw[curTileNo][DOWN]
        if not nextTileNo:
            return

        while jigsaw[nextTileNo][UP] != curTileNo:
            rotate_tile(nextTileNo)
        if edges[curTileNo][DOWN] != edges[nextTileNo][UP]:
            hflip_tile(nextTileNo)

        curTileNo = nextTileNo


def assemble_image(topLeftTileNo):
    curTileNo = topLeftTileNo
    curRowTileNo = topLeftTileNo

    while curRowTileNo:
        img_row = []
        for i in range(len(tiles[topLeftTileNo]) - 2):
            img_row.append([])
        while curTileNo:
            curTile = tiles[curTileNo]
            for i in range(len(img_row)):
                img_row[i] += curTile[i + 1][1:-1]
            curTileNo = jigsaw[curTileNo][RIGHT]

        for row in img_row:
            image.append(row)
        curRowTileNo = jigsaw[curRowTileNo][DOWN]
        curTileNo = curRowTileNo



def try_to_connect(tileNo, otherTileNo):
    for i, e in enumerate(edges[tileNo]):
        if jigsaw[tileNo][i]:
            continue
        for j, o in enumerate(edges[otherTileNo]):
            if jigsaw[otherTileNo][j]:
                continue

            if e == o:
                jigsaw[tileNo][i] = otherTileNo
                jigsaw[otherTileNo][j] = tileNo

            if e == flip_edge(o):
                jigsaw[tileNo][i] = otherTileNo
                jigsaw[otherTileNo][j] = tileNo


with open('./input.txt') as file:
    curTile = []
    while line := file.readline():
        line = line.rstrip()
        if line.startswith('Tile '):
            curTileID = int(re.sub(r'^Tile (\d+):$', r'\1', line))
        elif len(line) > 0:
            curTile.append(list(line.rstrip()))
        else:
            tiles[curTileID] = curTile
            curTile = []

# calc edges
for tileNo, tile in tiles.items():
    edges[tileNo] = store_edges(tile)

# initialize the connections map
jigsaw = {_: [None] * 4 for _ in edges.keys()}

# find all connections between tiles
for tileNo in edges.keys():
    for otherTileNo in [_ for _ in edges.keys() if _ != tileNo]:
        try_to_connect(tileNo, otherTileNo)

# pick one corner and start top left to complete the jigsaw
corners = [tileNo for (tileNo, connections) in jigsaw.items() if connections.count(None) == 2]
topLeftTileNo = corners[0]

while jigsaw[topLeftTileNo][UP] is not None or jigsaw[topLeftTileNo][LEFT] is not None:
    rotate_tile(topLeftTileNo)

complete_jigsaw(topLeftTileNo)
assemble_image(topLeftTileNo)

monster_raw = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """

monster = []
for y, row in enumerate(monster_raw.split('\n')[1:]):
    for x, c in enumerate(row):
        if c == '#':
            monster.append((y, x))

print_tiles()
print('='*96)
image = rotate_matrix(image)
print_tiles()
print('='*96)
image = rotate_matrix(image)
print_tiles()
print('='*96)
image = rotate_matrix(image)
print_tiles()

print(datetime.datetime.now() - begin_time)
