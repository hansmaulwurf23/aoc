import math
from itertools import combinations

from aopython import vector_add, vector_mul


class Particle:

    def __init__(self, id, vals):
        self.id = id
        self.position = tuple(vals[:3])
        self.velocity = tuple(vals[3:6])
        self.accelera = tuple(vals[6:])

        # initial position and velocity
        self.p0 = tuple(self.position)
        self.v0 = tuple(self.velocity)

    def tick(self):
        self.velocity = tuple(vector_add(self.velocity, self.accelera))
        self.position = tuple(vector_add(self.position, self.velocity))

    def v(self, t):
        return tuple(vector_add(self.v0, vector_mul(self.accelera, t)))

    def p(self, t):
        return tuple(vector_add(self.p0,
                                vector_add(vector_mul(self.v0, t), vector_mul(self.accelera, t * (t + 1) // 2))))

    def collides(self, other):
        t = [0] * 3
        for dim in range(3):
            dx = self.p0[dim] - other.p0[dim]
            dv = self.v0[dim] - other.v0[dim]
            da = self.accelera[dim] - other.accelera[dim]

            # linear equation dx + t * dv == 0
            if da == 0:
                if dv:
                    t[dim] = -dx / dv
                else:
                    t[dim] = None
                continue

            a = da
            b = da + 2 * dv
            c = 2 * dx
            b2 = pow(b, 2)
            ac4 = 4 * a * c

            # negative sqrt in x1/2 = -b ± sqrt(b^2 -4ac) // 2a
            if b2 < ac4:
                return -1

            t1 = (-b + pow(b2 - ac4, .5)) / (2 * a)
            t2 = (-b - pow(b2 - ac4, .5)) / (2 * a)

            t1 = t1 if t1.is_integer() else -1
            t2 = t2 if t2.is_integer() else -1

            if t1 <= 0:
                t[dim] = -1 if t2 <= 0 else int(t2)
            elif t1 < t2:
                t[dim] = int(t1)
            else:
                t[dim] = int(t1) if t2 <= 0 else int(t2)

        if all([m == n or m is None or n is None for m, n in combinations(t, 2)]):
            return list(filter(lambda x: x is not None, t))[0]
        else:
            return -1

    def center_distance(self):
        return sum(map(abs, self.position))

    def absolute_acceleration(self):
        return sum(map(abs, self.accelera))
