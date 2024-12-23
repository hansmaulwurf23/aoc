import datetime
from itertools import combinations
import pydot
from collections import defaultdict

begin_time = datetime.datetime.now()


def render_graph(filename='graph.svg'):
    global network
    graph = pydot.Dot("Network", graph_type="graph")
    for node, conns in network.items():
        graph.add_node(pydot.Node(node, style='filled'))
        for c in [c for c in conns if c == min(node, c)]:
            graph.add_edge(pydot.Edge(node, c, color='black'))
    graph.write_svg(filename)


def get_sub_graph(network, v):
    subg = {v} | network[v]
    for o in network[v]:
        if subg & (network[o] - {v}):
            subg = subg & ({o} | network[o])
    return subg


network = defaultdict(set)
with open('./example.txt') as f:
    while line := f.readline().rstrip():
        a, b = line.split('-')
        network[a].add(b)
        network[b].add(a)

render_graph('example.svg')
groups = set()
for k, others in [(k, os) for k, os in network.items() if k[0] == 't']:
    for a, b in [(a, b) for a, b in combinations(others, 2) if b in network[a]]:
        groups.add(frozenset({k, a, b}))

print(f'part 1: {len(groups)}')

max_len, max_subg = None, None
for v in network:
    subg = get_sub_graph(network, v)
    if max_len is None or len(subg) > max_len:
        max_len, max_subg = len(subg), subg

print(f'part 2: {','.join(sorted(max_subg))}')
print(datetime.datetime.now() - begin_time)
