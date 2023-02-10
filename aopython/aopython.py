import math


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


def manhattan_distance(source, target=None):
    """
    calculates the manhattan distance of the given coords to the center of the dimensions
    :param source: n-dimensional iterable holding the coordinates
    :params target: optional n-dimensional iterable holding the target coordinates
    :return: manhattan distance to the center of the coordinate system
    """
    if target is None:
        target = [0] * len(source)

    return sum([abs(s - t) for s, t in zip(source, target)])


def range_in_range(a, b):
    return a.start in b and a.stop - 1 in b


def vector_add(a, b):
    """
    Adds two vectors
    """
    return [m + n for m, n in zip(a, b)]


def vector_mul(a, b):
    """
    Scales every dimension of vector a with the factor b
    """
    return [m * b for m in a]


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


def last_digit(n):
    if n < 0:
        return -n % 10
    else:
        return n % 10


def bool_list_to_int(l):
    return sum(v << i for i, v in enumerate(reversed(l)))


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def divisors(number):
    # get factors and their counts
    factors = {}
    rest = number
    p = 2
    while p * p <= rest:
        while rest % p == 0:
            factors[p] = factors.get(p, 0) + 1
            rest //= p
        p += 1
    if rest > 1:
        factors[rest] = factors.get(rest, 0) + 1

    primes = list(factors.keys())

    # generates factors from primes[k:] subset
    def generate(k):
        if k == len(primes):
            yield 1
        else:
            rest = generate(k + 1)
            prime = primes[k]
            for factor in rest:
                prime_to_i = 1
                # prime_to_i iterates prime**i values, i being all possible exponents
                for _ in range(factors[prime] + 1):
                    yield factor * prime_to_i
                    prime_to_i *= prime

    yield from generate(0)


def divisors_sorted(num):
    divs = [i for i in range(1, int(math.sqrt(num)) + 1) if num % i == 0]
    return divs + [num // i for i in reversed(divs) if i != num // i]
