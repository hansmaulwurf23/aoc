import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


def scatter(points, *, marker='s', c='#1f77b4', s=160):
    x = list(map(lambda x: x[0], points))
    y = list(map(lambda x: x[1], points))
    plt.scatter(x, y, s=s, c=c, marker=marker)


def show_grid(points, highlights=None, marker='s', c='#1f77b4', s=160, minTicks=True, highlightsize=15, no_show=False,
              fh=10, fw=10, invert_yaxis=False, xrange=None, yrange=None, title=None):
    fig, ax = plt.subplots()
    fig.set(figwidth=fw, figheight=fh, dpi=100)

    if minTicks:
        ax.minorticks_on()

    if invert_yaxis:
        matplotlib.axes.Axes.invert_yaxis(ax)

    scatter(points, marker=marker, s=s, c=c)

    if isinstance(highlights, list) or isinstance(highlights, set):
        scatter(highlights, marker=marker, s=(highlightsize or s), c='r')
    elif isinstance(highlights, dict):
        for color, points in highlights.items():
            if isinstance(points, dict):
                for k, coords in points.items():
                    scatter([coords], marker=f'${k}$', s=(highlightsize or s), c=color)
            else:
                scatter(points, marker=marker, s=(highlightsize or s), c=color)


    plt.grid(True)
    plt.grid(True, which='minor')

    if xrange is not None:
        plt.xlim(xrange)
    if yrange is not None:
        plt.ylim(yrange)

    if title is not None:
        plt.title(title)

    if not no_show:
        plt.show()
    return plt


def show_heatmap(points, highlights=None, marker='s', s=160):
    colors = list(map(lambda x: x[2], points))
    show_grid(points, highlights=highlights, marker=marker, c=colors, s=s)


def pcolormesh(points, cmap=None, fh=10, fw=10, x=None, y=None):
    fig, ax = plt.subplots()
    fig.set(figwidth=fw, figheight=fh, dpi=100)
    if cmap is not None:
        cmap = ListedColormap(cmap)
    if x and y:
        plt.pcolormesh(x, y, points, cmap=cmap)
    else:
        plt.pcolormesh(points, cmap=cmap)
    plt.show()


def plot_xy(data):
    x = list(map(lambda x: x[0], data))
    y = list(map(lambda x: x[1], data))
    plt.plot(x, y)
    plt.show()


def hex_grid(data, fh=10, fw=10):
    fig, ax = plt.subplots()
    fig.set(figwidth=fw, figheight=fh, dpi=100)
    x = list(map(lambda x: x[0], data))
    y = list(map(lambda x: x[1], data))
    plt.hexbin(x, y)
    plt.show()


def voxels(data, fh=10, fw=10):
    range_x = range(min(map(lambda e: e[0], data)), max(map(lambda e: e[0], data)))
    range_y = range(min(map(lambda e: e[1], data)), max(map(lambda e: e[1], data)))
    range_z = range(min(map(lambda e: e[2], data)), max(map(lambda e: e[2], data)))
    grid = np.zeros(shape=(len(range_x)+1, len(range_y)+1, len(range_z)+1), dtype=int)

    for d in data:
        grid.itemset(d, True)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    fig.set(figwidth=fw, figheight=fh, dpi=100)
    ax.voxels(grid, edgecolor='k', facecolors='#7A88CCC0', )

    # ax.set(xticklabels=[],
    #        yticklabels=[],
    #        zticklabels=[])

    plt.show()
