import datetime
from collections import deque, defaultdict
from functools import reduce

import pydot

from aopython import dotdict, vector_add, gcd, lcm

begin_time = datetime.datetime.now()

LO, HI = range(2)
INV = [HI, LO]
BRDCSTR = 'broadcaster'
FLPFLP = '%'
CONJ = '&'
OUTPUT = 'output'

def render_graph():
    global modules
    graph = pydot.Dot("PulsePropagation", graph_type="digraph")
    for mod, modinfo in modules.items():
        graph.add_node(pydot.Node(mod, shape=("circle" if modinfo.type == FLPFLP else 'box'), style='filled'))
        for t in modinfo.targets:
            graph.add_edge(pydot.Edge(mod, t, ))

    # rx not a source
    graph.add_node(pydot.Node('rx', shape="diamond", style='filled', fillcolor="red"))

    rx_in = [n for n in modules if 'rx' in modules[n].targets][0]
    graph.get_node(rx_in)[0].set('fillcolor', 'yellow')

    for n in set([n for n in modules if rx_in in modules[n].targets]):
        graph.get_node(n)[0].set('fillcolor', 'green')

    graph.write_png("graph.png")


def run_to_rx():
    global modules
    # predecessor of rx
    rx_in = [n for n in modules if 'rx' in modules[n].targets][0]
    # what triggers the predecessors of rx
    rx_in_ins = set([n for n in modules if rx_in in modules[n].targets])
    first_seen = {}

    steps = 0

    while True:
        steps += 1
        comm = deque([(BRDCSTR, LO, 'button')])

        while comm:
            mod, sgnl, src = comm.popleft()
            # print(f'{src} -{"high" if sgnl else "low"}-> {mod}')

            if mod == rx_in and sgnl == HI:
                if src not in first_seen:
                    first_seen[src] = steps

                    # all cycles found
                    if first_seen.keys() == rx_in_ins:
                        return reduce(lambda a, b: lcm(a, b), first_seen.values())

            if mod == BRDCSTR:
                for t in modules[BRDCSTR].targets:
                    comm.append((t, sgnl, mod))
            elif mod == OUTPUT:
                # print(sgnl, src)
                pass
            elif mod not in modules:
                continue
            elif modules[mod].type == FLPFLP and sgnl == LO:
                modules[mod].state = INV[modules[mod].state]
                for t in modules[mod].targets:
                    comm.append((t, modules[mod].state, mod))
            elif modules[mod].type == CONJ:
                modules[mod].state[src] = sgnl
                s = LO if all(modules[mod].state.values()) else HI
                for t in modules[mod].targets:
                    comm.append((t, s, mod))


def reset_state(cons):
    global modules
    for mod, minf in modules.items():
        if minf.type == FLPFLP:
            minf.state = LO
        for t in [t for t in minf.targets if t in cons]:
            cons[t][mod] = LO

    for mod, sources in cons.items():
        modules[mod].state = sources


modules = {}
with open('./input.txt') as f:
    cons = {}
    while line := f.readline().rstrip():
        mod, targets = line.split(' -> ')
        kind = mod[0] if mod != BRDCSTR else BRDCSTR
        mod = mod if mod == BRDCSTR else mod[1:]
        modules[mod] = dotdict({'type': kind, 'targets': targets.split(', ')})
        if kind == CONJ:
            cons[mod] = dict()

reset_state(cons)
# render_graph()
p2 = run_to_rx()
print(f'part 2: {p2}')
assert p2 in (207787533680413, )
print(datetime.datetime.now() - begin_time)
