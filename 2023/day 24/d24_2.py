from aopython import vector, vector_mul
import datetime

begin_time = datetime.datetime.now()

X, Y, Z = range(3)
P, V = range(2)

def cross_product(a, b):
    return a[Y] * b[Z] - a[Z] * b[Y], a[Z] * b[X] - a[X] * b[Z], a[X] * b[Y] - a[Y] * b[X]

def scalar_product(a, b):
    return a[X] * b[X] + a[Y] * b[Y] + a[Z] * b[Z]

def matrix_vector_prod(M, v):
    return tuple(scalar_product(row, v) for row in zip(*M))

hailstones = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        pos, v = line.split(' @ ')
        hailstones.append([list(map(int, pos.split(', '))), list(map(int, v.split(', ')))])

h1 = hailstones[0]
for i, h2 in enumerate(hailstones[1:], 1):
    # Geschwindigkeitsvektoren duerfen nicht linear abhaenig sein, sonst kann daraus keine Ebene gemacht werden
    # https://www.mathe-online.at/materialien/Andreas.Pester/files/Vectors/lineare_abhaengigkeit.htm
    if any(v != 0 for v in cross_product(h1[V], h2[V])):
        break
for h3 in hailstones[i + 1:]:
    if any(v != 0 for v in cross_product(h1[V], h3[V])) and any(v != 0 for v in cross_product(h2[V], h3[V])):
        break

# https://de.wikipedia.org/wiki/Schnittgerade#Schnitt_zweier_Ebenen_in_Parameterform
p12 = vector(h2[P], h1[P])
a = cross_product(p12, vector(h2[V], h1[V]))
A = scalar_product(p12, cross_product(h1[V], h2[V]))
p23 = vector(h3[P], h2[P])
b = cross_product(p23, vector(h3[V], h2[V]))
B = scalar_product(p23, cross_product(h2[V], h3[V]))
p31 = vector(h1[P], h3[P])
c = cross_product(p31, vector(h3[V], h1[V]))
C = scalar_product(p31, cross_product(h1[V], h3[V]))

# https://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection
rv = matrix_vector_prod((cross_product(b, c), cross_product(c, a), cross_product(a, b)), (A, B, C))
# time is the integer offset to origin of h1
t = scalar_product(a, cross_product(b, c))
rv = vector_mul(rv, 1 / t)
print(rv)

# for any hailstone h the rock with pos rp and velocity rv will hit if
#    rp + t * rv = h[P] + h[V] * t
# -> rp = h[P] + t * (h[V] - rv)
v1 = vector(rv, h1[V])
v2 = vector(rv, h2[V])
vv = cross_product(v1, v2)

# https://de.wikipedia.org/wiki/Spatprodukt
A = scalar_product(vv, cross_product(h2[P], vector(rv, h2[V])))
B = scalar_product(vv, cross_product(h1[P], vector(h1[V], rv)))
C = scalar_product(h1[P], vv)
# https://www.mathi.uni-heidelberg.de/~flemmermeyer/HA/skalar-kreuz.pdf
S = scalar_product(vv, vv)

rp = matrix_vector_prod((v1, v2, vv), (A, B, C))

p2 = int(sum(rp) / S)
print(p2)
assert p2 in [566373506408017]
print(datetime.datetime.now() - begin_time)