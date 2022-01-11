import datetime
import re
from functools import reduce

begin_time = datetime.datetime.now()

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

tiles = dict()
edges = dict()
jigsaw = dict()

def edge_to_int(edge):
    return int(''.join(['1' if it == '#' else '0' for it in edge]), 2)


def flip_edge(edge):
    return int(''.join(reversed(list(f'{edge:010b}'))), 2)


def store_edges(tile):
    result = [None] * 4
    result[UP] = edge_to_int(tile[0])
    result[DOWN] = edge_to_int(tile[-1])
    result[LEFT] = edge_to_int([it[0] for it in [row for row in tile]])
    result[RIGHT] = edge_to_int([it[-1] for it in [row for row in tile]])

    return result


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
jigsaw = {x: [None] * 4 for x in edges.keys()}

for tileNo in edges.keys():
    for otherTileNo in [t for t in edges.keys() if t != tileNo]:
        try_to_connect(tileNo, otherTileNo)

corners = [tileNo for (tileNo, connections) in jigsaw.items() if connections.count(None) == 2]
print(reduce((lambda x, y: x * y), corners))
print(datetime.datetime.now() - begin_time)
