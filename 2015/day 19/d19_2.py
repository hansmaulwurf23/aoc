import datetime
from collections import defaultdict

import math
from functools import cache

import pydot

begin_time = datetime.datetime.now()

def print_graph(graph):
    g = pydot.Dot()
    for node, targets in graph.items():
        for target in targets:
            g.add_edge(pydot.Edge(node, target))
    g.write_png("graph.png")

@cache
def reverse(mol: str):
    global revs
    if mol == 'e':
        return 0

    min_steps = math.inf
    for target, source in revs:
        if target in mol:
            min_steps = min(min_steps, 1 + reverse(mol.replace(target, source)))

    print(len(mol), min_steps)
    return min_steps

reactions = defaultdict(list)
# reverse is unique
revs = dict()
molecule = None
with open('./input.txt') as f:
    lines = [line.rstrip() for line in f.readlines()]
    for line in lines[:-2]:
        f, t = line.split(' => ')
        reactions[f].append(t)
        revs[t] = f

    molecule = lines[-1]

# convert revs to a tuple list ordered by descending lengths
revs = list(sorted([tuple([k, v]) for k, v in revs.items()], key=lambda x: -len(x[0])))

print(reverse(molecule))
print(datetime.datetime.now() - begin_time)
