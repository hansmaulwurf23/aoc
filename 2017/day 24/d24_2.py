import datetime
from collections import defaultdict

begin_time = datetime.datetime.now()

components = set()
ports = defaultdict(set)
starter = {}


def compatibles(comps, open_pin):
    global ports
    return ports[open_pin] & comps


def strength(unused_comp):
    used = components - unused_comp
    return sum([a + b for a, b in used])


def bfs(starter):
    global components

    other = starter[0] if starter[1] == 0 else starter[1]

    q = [(other, components - {starter})]
    max_strength = None
    max_length = 0
    while q:
        open_pin, unused_comp = q.pop()
        comps = compatibles(unused_comp, open_pin)
        if not comps:
            length = len(components) - len(unused_comp)
            val = strength(unused_comp)
            if length >= max_length:
                if length > max_length:
                    max_length = length
                    max_strength = None
                if max_strength is None or val > max_strength:
                    max_strength = val

        for compatible in comps:
            q.append((compatible[0] if compatible[0] != open_pin else compatible[1], unused_comp - {compatible}))
    return max_length, max_strength


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        c = tuple(map(int, line.split('/')))
        if 0 in c:
            starter = c
        components.add(c)
        ports[c[0]].add(c)
        ports[c[1]].add(c)

print(bfs(starter))
print(datetime.datetime.now() - begin_time)
