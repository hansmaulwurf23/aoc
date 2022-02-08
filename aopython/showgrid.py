import matplotlib.pyplot as plt


def show_grid(points, highlights=None, marker='s', c='#1f77b4', s=160):
    fig, ax = plt.subplots()
    fig.set(figwidth=10, figheight=10, dpi=100)

    ax.minorticks_on()

    x = list(map(lambda x: x[0], points))
    y = list(map(lambda x: x[1], points))
    plt.scatter(x, y, s=s, c=c, marker=marker)

    if highlights:
        x = list(map(lambda x: x[0], highlights))
        y = list(map(lambda x: x[1], highlights))
        plt.scatter(x, y, s=s, c='r', marker=marker)


    plt.grid(True)
    plt.grid(True, which='minor')
    plt.show()


def show_heatmap(points, highlights=None, marker='s', s=160):
    colors = list(map(lambda x: x[2], points))
    show_grid(points, highlights=highlights, marker=marker, c=colors, s=s)

