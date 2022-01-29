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


def vector_add(a, b):
    """
    Adds two vectors
    """
    return [m + n for m, n in zip(a, b)]


def vector(from_point, to_point):
    """
    Creates a new vector from from_point to to_point
    """
    return [m - n for m, n in zip(to_point, from_point)]


def vector_inv(v):
    return [-m for m in v]


def vector_sgn(v):
    """
    Returns a new vector which holds the sign(c) for c in every dimension
    :param v: vector [c1, c2, ...]
    :return: new vector [sign(c1), sign(c2), ...]
    """
    return [sign(m) for m in v]


def vector_abs(v):
    """
    Returns a new vector with all absolute values from the given vector
    :param v: [c1, c2, ...]
    :return: [abs(c1), abs(c2), ...]
    """
    return [abs(m) for m in v]


def cmp(a, b):
    """
    Returns 1 if a > b, 0 if a == b, -1 if a < b
    """
    return (a > b) - (a < b)


def sign(a):
    return (a > 0) - (a < 0)


def ceildiv(a, b):
    return -(a // -b)


def gcd(a, b):
    while b != 0:
        (a, b) = (b, a % b)
    return a


def lcm(a, b):
    return abs(a * b) // gcd(a, b)

