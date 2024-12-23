import math
from itertools import zip_longest


def min_max(values):
    lo, hi = None, None
    for v in values:
        if lo is None or lo > v: lo = v
        if hi is None or hi < v: hi = v

    return lo, hi


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

def print_grid(grid, sep_below=False):
    print('\n'.join([''.join(line) for line in grid]))
    if sep_below:
        print('='*80)

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


def merge_ranges(ranges: list):
    """
    Merges a list of ranges. Returns a list of overlapping free sorted by start ranges.
    """
    res = []
    for r in sorted(ranges, key=lambda r: r.start):
        if len(res):
            p = res[-1]
            if r.start in p:
                res[-1] = range(p.start, max(p.stop, r.stop))
            else:
                res.append(r)
        else:
            res.append(r)

    return res


def intersect_ranges(x: range, y: range):
    """
    Returns a new range that contains the intersection of the two given ranges
    """
    assert x.step == y.step == 1
    return range(max(x.start, y.start), min(x.stop, y.stop))


def abc_formula(a, b, c):
    """
    Solves a quadratic function ax^2 + bx + c = 0. Negative discriminant will return no solution (instead of complex
    solutions). Upon a == 0 the linear function is solved.
    """
    if a == 0:
        return [-c/b]

    discriminant = b * b - (4 * a * c)
    if discriminant < 0:
        return []

    sqrt_discr = pow(discriminant, .5)
    sol_1 = (-b + sqrt_discr) / (2 * a)

    if discriminant == 0:
        return [sol_1]

    sol_2 = (-b - sqrt_discr) / (2 * a)
    return list(sorted([sol_1, sol_2]))


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


def mapSum(coutings, updates):
    if not updates: return coutings

    for k, v in updates.items():
        coutings[k] += v
    return coutings


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


def triangular_number(n: int) -> int:
    return n * (n + 1) // 2


def solve(coeffs: list, rs: list) -> list:
    """ Solve n linear equations with n unknowns.
        a11 x + a12 y + a13 z + ... = r1
        ...
        an1 x + an2 y + an3 z + ... = rn

        Pass coefficients in list of lists:
        [[a11, a12, a13, ..., a1n], ..., [an1, an2, an3, ..., ann]]
        and the right sides as another list:
        [r1, r2, ..., rn]

        Returns solution for [x, y, z, ...]
        """

    # transform to equations like this: a*x + b*y + c*z + ... - r = 0
    eqs = []
    for cs, r in zip(coeffs, rs):
        eqs.append(cs + [-r])

    remaining_eqs = []
    while eqs:
        # find an equation whose first element is not zero
        eq, idx = next((e, i) for i, e in enumerate(eqs) if e[0] != 0)
        # add this equation with the non zero first element eliminated
        eq = [-coeff / eq[0] for coeff in eq[1:]]
        remaining_eqs.append(eq)
        eqs.pop(idx)

        # eliminate first element from all other equations
        for other_eq in eqs:
            for j, coeff in enumerate(eq):
                other_eq[j + 1] += other_eq[0] * coeff
            other_eq.pop(0)

    solutions = [remaining_eqs.pop(-1)[0]]
    for i, eq in enumerate(reversed(remaining_eqs)):
        solutions.append(sum([a * b for a, b in zip_longest(eq, reversed(solutions), fillvalue=1)]))
    solutions.reverse()

    return solutions


def int_solve(coeffs, rs):
    """ see :func:`~solve` for description of arguments
        returns None in all dimensions if there is no integer solution
    """
    solutions = solve(coeffs, rs)

    solutions = list(map(lambda x: int(x + .5), solutions))
    for cs, r in zip(coeffs, rs):
        if sum([c * a for c, a in zip(cs, solutions)]) != r:
            return [None] * len(rs)

    return solutions
