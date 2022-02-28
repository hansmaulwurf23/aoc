import datetime
import re

from matplotlib import pyplot as plt, ticker
from matplotlib.colors import ListedColormap
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
    res = []

    for y in range(lowest_y - 3, ty + 3):
        row = []
        for x in range(fx - 2, tx + 1):
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
                        x=range(fx - 2, tx+1), y=range(lowest_y - 3, ty+3))


def fill_basin_line(start_pos):
    cur_pos = start_pos
    min_x, max_x = cur_pos[0], cur_pos[0]
    drop_right, drop_left = False, False
    new_wet_tiles = set()
    new_wet_tiles.add(cur_pos)

    if cur_pos in wet_tiles:
        wet_tiles.remove(cur_pos)

    while (d := neighbor(cur_pos, RIGHT)) not in clay:
        if neighbor(d, DOWN) not in clay and neighbor(d, DOWN) not in resting_water:
            drop_right = True
            break
        cur_pos = d
        max_x = d[0]
        new_wet_tiles.add(cur_pos)

    cur_pos = start_pos
    while (d := neighbor(cur_pos, LEFT)) not in clay:
        if neighbor(d, DOWN) not in clay and neighbor(d, DOWN) not in resting_water:
            drop_left = True
            break
        cur_pos = d
        min_x = d[0]
        new_wet_tiles.add(cur_pos)

    if drop_right or drop_left:
        wet_tiles.update(new_wet_tiles)
    else:
        resting_water.update(new_wet_tiles)

    return min_x, max_x, drop_left, drop_right


def water_flow(start_pos):
    if start_pos[1] <= lowest_y:
        return

    flow_pos = start_pos
    # flow until we reach clay
    wet_tiles.add(flow_pos)
    while True:
        new_pos = neighbor(flow_pos, DOWN)
        if new_pos[1] < lowest_y:
            return
        if new_pos in wet_tiles:
            return
        if new_pos not in clay:
            flow_pos = new_pos
            wet_tiles.add(flow_pos)
            continue
        break

    min_x, max_x, drop_left, drop_right = fill_basin_line(flow_pos)
    while not drop_right and not drop_left:
        flow_pos = neighbor(flow_pos, UP)
        min_x, max_x, drop_left, drop_right = fill_basin_line(flow_pos)

    if drop_right:
        water_flow(tuple([max_x + 1, flow_pos[1]]))

    if drop_left:
        water_flow(tuple([min_x - 1, flow_pos[1]]))


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        fix, low, high = list(map(int, re.findall(r'\d+', line)))
        if line.startswith('x'):
            clay |= {(fix, -y) for y in range(low, high+1)}
        else:
            clay |= {(x, -fix) for x in range(low, high+1)}

fx, tx, lowest_y, ty = min_max_2d(clay)
water_flow((500, 0))

# remove dropping into sand fields after water_flow(..) is done to keep code clean
for y in range(0, max(clay, key=lambda x:x[1])[1], -1):
    if (500, y) in wet_tiles:
        wet_tiles.remove((500, y))

wet_tiles -= resting_water
plot()
print(len(wet_tiles | resting_water))
print(datetime.datetime.now() - begin_time)
