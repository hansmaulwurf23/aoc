def min_max_2d(coords):
    """
    Calculates the min and max of every dimension in 2D
    :param coords: iterable holding [x, y] (or vice versa)
    :return: min_x, max_x, min_y, max_y (or vice versa, as u map)
    """
    fx, tx, fy, ty = [None] * 4
    for c in coords:
        if tx is None or c[0] > tx:
            tx = c[0]
        if fx is None or c[0] < fx:
            fx = c[0]
        if ty is None or c[1] > ty:
            ty = c[1]
        if fy is None or c[1] < fy:
            fy = c[1]

    return fx, tx, fy, ty


def manhattan_distance(coords):
    """
    calculates the manhattan distance of the given coords to the center of the dimensions
    :param coords: n-dimensional iterable holding the coordinates
    :return: manhattan distance to the center of the coordinate system
    """
    return sum([abs(c) for c in coords])
