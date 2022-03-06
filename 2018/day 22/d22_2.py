import datetime
import heapq
import re

from aopython import vector_add

begin_time = datetime.datetime.now()
depth = None
target = None
mouth = (0, 0)
geolo_cache = dict()
ROCKY, WET, NARROW = range(3)
ERO, GEO, RISK = range(3)
TORCH, GEAR, NEITHER = range(3)
symbols = {ROCKY: '.', WET: '=', NARROW: '|'}
equipment = {ROCKY: {TORCH, GEAR}, WET: {GEAR, NEITHER}, NEITHER: {TORCH, NEITHER}}
purpose = {TORCH: {ROCKY, NARROW}, GEAR: {ROCKY, WET}, NEITHER: {WET, NARROW}}
MAGICMOD = 20183
ADDITIONAL = 1000


def dijkstra(grid, start, target):
    # state is current_minutes, current_position, current_equipment
    start_state = 0, start, TORCH
    pq = [start_state]
    best = dict()
    while pq:
        cur_mins, cur_pos, cur_equip = heapq.heappop(pq)

        if (cur_pos, cur_equip) in best and best[(cur_pos, cur_equip)] <= cur_mins:
            continue
        best[(cur_pos, cur_equip)] = cur_mins

        cx, cy = cur_pos
        cur_type = grid[cy][cx][RISK]
        alt_equip = (equipment[cur_type] - {cur_equip}).pop()

        # just in case change equipment
        heapq.heappush(pq, (cur_mins + 7, cur_pos, alt_equip))

        if (cur_pos, cur_equip) == (target, TORCH):
            print(cur_mins)
            break

        for new_pos in adjacents(cur_pos):
            nx, ny = new_pos
            new_equip, new_type = cur_equip, grid[ny][nx][RISK]
            if cur_equip in equipment[new_type]:
                heapq.heappush(pq, (cur_mins + 1, new_pos, cur_equip))


def adjacents(pos):
    res = []
    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, 1)]:
        ax, ay = pos[0] + dx, pos[1] + dy
        if 0 <= ax and 0 <= ay:
            res.append((ax, ay))

    return res


def build_map(topleft, bottomright):
    sx, sy = topleft
    tx, ty = bottomright
    grid = []
    for y in range(sy, ty + ADDITIONAL + 1):
        grid.append([])
        for x in range(sx, tx + ADDITIONAL + 1):
            if (x, y) == topleft or (x, y) == bottomright:
                geo = 0
            elif y == 0:
                geo = x * 16807
            elif x == 0:
                geo = y * 48271
            else:
                geo = grid[y - 1][x][ERO] * grid[y][x - 1][ERO]

            ero = (geo + depth) % MAGICMOD
            risk = ero % 3
            grid[-1].append((ero, geo, risk))

    print(f'finished building grid after {datetime.datetime.now() - begin_time}')
    return grid


with open('./input.txt') as f:
    lines = f.readlines()
    depth = list(map(int, re.findall(r'\d+', lines[0])))[0]
    target = tuple(map(int, re.findall(r'\d+', lines[1])))

dijkstra(build_map(mouth, target), mouth, target)
print('1073 too high')
print(datetime.datetime.now() - begin_time)
