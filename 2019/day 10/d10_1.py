import datetime

begin_time = datetime.datetime.now()
asteroids = []


def gcd(a, b):
    while b != 0:
        (a, b) = (b, a % b)
    return a


def find_line_of_sights(asteroids):
    line_of_sights = dict()
    for a in asteroids:
        line_of_sights[a] = set()
        for o in [_ for _ in asteroids if _ != a]:
            # calc vector between asteroids a and o
            vector = [o[0] - a[0], o[1] - a[1]]
            # reduce the fraction (aka direction)
            divisor = gcd(abs(vector[0]), abs(vector[1]))
            vector = (vector[0] / divisor, vector[1] / divisor)
            # since value of dict is a set we don't store same line of sight twice
            line_of_sights[a].add(vector)

    return line_of_sights


with open('./input.txt') as f:
    y = 0
    while line := f.readline().rstrip():
        asteroids.extend([(x, y) for x, c in enumerate(line) if c == '#'])
        y += 1


line_of_sights = find_line_of_sights(asteroids)
# best asteroid is the one with the most directions
besteroid = max(line_of_sights, key=(lambda k: len(line_of_sights[k])))
print(len(line_of_sights[besteroid]))
print(datetime.datetime.now() - begin_time)
