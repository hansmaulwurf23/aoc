import matplotlib.pyplot as plt


def show_grid(points, highlights=None, marker='s'):
    fig, ax = plt.subplots()
    fig.set(figwidth=10, figheight=10, dpi=100)

    ax.minorticks_on()

    x = list(map(lambda x: x[0], points))
    y = list(map(lambda x: x[1], points))
    plt.scatter(x, y, s=160, marker=marker)

    if highlights:
        x = list(map(lambda x: x[0], highlights))
        y = list(map(lambda x: x[1], highlights))
        plt.scatter(x, y, s=160, c='r', marker=marker)


    plt.grid(True)
    plt.grid(True, which='minor')
    plt.show()

