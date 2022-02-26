import datetime
import re
import showgrid
from aopython import vector_add, min_max_2d

begin_time = datetime.datetime.now()

DOWN, UP, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)

clay = set()
wet_tiles = set()
resting_water = set()

def neighbor(pos, delta):
    return tuple(vector_add(pos, delta))


def plot():
    showgrid.show_grid(clay, highlights={'lightgreen': wet_tiles, 'lightblue': resting_water},
                       highlightsize=6, c='gray', s=6, fh=100)


def water_flow(start_pos):
    flow_pos = start_pos
    # flow until we reach clay
    wet_tiles.add(flow_pos)
    while (d := neighbor(flow_pos, DOWN)) not in clay:
        flow_pos = d
        wet_tiles.add(flow_pos)

    # fill basin, first right then left to infer outermost positions
    rest_pos = flow_pos
    min_x, max_x = flow_pos[0], flow_pos[0]
    resting_water.add(rest_pos)
    while (d := neighbor(rest_pos, RIGHT)) not in clay:
        rest_pos = d
        max_x = d[0]
        resting_water.add(rest_pos)

    rest_pos = flow_pos
    while (d := neighbor(rest_pos, LEFT)) not in clay:
        rest_pos = d
        min_x = d[0]
        resting_water.add(rest_pos)

    contained = True
    while contained:
        flow_pos = tuple(neighbor(flow_pos, UP))
        rest_pos = flow_pos
        resting_water.add(rest_pos)
        while rest_pos[0] < max_x:
            rest_pos = tuple(neighbor(rest_pos, RIGHT))
            if rest_pos in clay:
                max_x = rest_pos[0] - 1
                break
            resting_water.add(rest_pos)
        if neighbor(rest_pos, RIGHT) not in clay:
            contained = False
            water_flow(neighbor(neighbor(rest_pos, RIGHT), RIGHT))

        rest_pos = flow_pos
        while rest_pos[0] > min_x:
            rest_pos = tuple(neighbor(rest_pos, LEFT))
            if rest_pos in clay:
                min_x = rest_pos[0] + 1
                break
            resting_water.add(rest_pos)
        if neighbor(rest_pos, LEFT) not in clay:
            contained = False
            water_flow(neighbor(neighbor(rest_pos, LEFT), LEFT))



with open('./input.txt') as f:
    while line := f.readline().rstrip():
        fix, low, high = list(map(int, re.findall(r'\d+', line)))
        if line.startswith('x'):
            clay |= {(fix, -y) for y in range(low, high+1)}
        else:
            clay |= {(x, -fix) for x in range(low, high+1)}

fx, tx, lowest_y, ty = min_max_2d(clay)
# showgrid.show_grid(clay, s=6, fh=100)
water_flow((500, 0))
print(datetime.datetime.now() - begin_time)
