import datetime
import re

from matplotlib import pyplot as plt, ticker
from matplotlib.colors import ListedColormap

import showgrid
from aopython import vector_add, min_max_2d

begin_time = datetime.datetime.now()

DOWN, UP, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)

clay = set()
wet_tiles = set()
resting_water = set()


def neighbor(pos, delta):
    return tuple(vector_add(pos, delta))


def do_plot(points, cmap=None, fh=10, fw=10, x=None, y=None):
    fig, ax = plt.subplots()
    fig.set(figwidth=fw, figheight=fh, dpi=100)
    ax.minorticks_on()
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_minor_formatter(ticker.ScalarFormatter())
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.secondary_xaxis('top')
    if cmap is not None:
        cmap = ListedColormap(cmap)
        plt.pcolormesh(x, y, points, cmap=cmap)

    plt.grid(True)
    plt.grid(True, which='minor')
    plt.show()


def plot():
    # showgrid.show_grid(clay, highlights={'lightgreen': wet_tiles, 'lightblue': resting_water},
    #                    highlightsize=6, c='gray', s=6, fh=100)
    res = []

    for y in range(lowest_y, ty + 1):
        row = []
        for x in range(fx, tx + 1):
            val = 0
            if (x, y) in clay:
                val = 1
            elif (x, y) in wet_tiles:
                val = 2
            elif (x, y) in resting_water:
                val = 3
            row.append(val)
        res.append(row)

    do_plot(res, fh=100, cmap=['white', 'darkgrey', 'blue', 'lightblue'],
                        x=range(fx, tx+1), y=range(lowest_y, ty+1))

def fill_basin_line(start_pos):
    cur_pos = start_pos
    min_x, max_x = cur_pos[0], cur_pos[0]
    drop_right, drop_left = False, False
    resting_water.add(cur_pos)
    wet_tiles.remove(cur_pos)
    while(d := neighbor(cur_pos, RIGHT)) not in clay:
        if neighbor(d, DOWN) not in clay:
            drop_right = True
            break
        cur_pos = d
        max_x = d[0]
        resting_water.add(cur_pos)

    cur_pos = start_pos
    while (d := neighbor(cur_pos, LEFT)) not in clay:
        if neighbor(d, DOWN) not in clay:
            drop_left = True
            break
        cur_pos = d
        min_x = d[0]
        resting_water.add(cur_pos)

    return min_x, max_x, drop_left, drop_right


def water_flow(start_pos):
    if start_pos[1] <= lowest_y:
        return

    flow_pos = start_pos
    # plot()
    # flow until we reach clay
    wet_tiles.add(flow_pos)
    while True:
        if (d := neighbor(flow_pos, DOWN)) not in clay and d not in wet_tiles:
            flow_pos = d
            wet_tiles.add(flow_pos)
            continue
        if d[1] < lowest_y:
            return
        break

    # fill basin, first right then left to infer outermost positions
    rest_pos = flow_pos
    min_x, max_x = flow_pos[0], flow_pos[0]
    resting_water.add(rest_pos)
    while (d := neighbor(rest_pos, RIGHT)) not in clay:
        if neighbor(d, DOWN) not in clay:
            return water_flow(d)
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
            wet_tiles.add(neighbor(rest_pos, RIGHT))
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
            wet_tiles.add(neighbor(rest_pos, LEFT))
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
plot()
print(datetime.datetime.now() - begin_time)
