import matplotlib.pyplot as plt


def scatter(points, *, marker='s', c='#1f77b4', s=160):
    x = list(map(lambda x: x[0], points))
    y = list(map(lambda x: x[1], points))
    plt.scatter(x, y, s=s, c=c, marker=marker)


def show_grid(points, highlights=None, marker='s', c='#1f77b4', s=160, minTicks=True, highlightsize=15):
    fig, ax = plt.subplots()
    fig.set(figwidth=10, figheight=10, dpi=100)

    if minTicks:
        ax.minorticks_on()

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
    plt.show()


def show_heatmap(points, highlights=None, marker='s', s=160):
    colors = list(map(lambda x: x[2], points))
    show_grid(points, highlights=highlights, marker=marker, c=colors, s=s)

