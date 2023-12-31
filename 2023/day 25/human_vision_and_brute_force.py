import concurrent.futures
import datetime
from collections import defaultdict
from functools import reduce
# import pydot

begin_time = datetime.datetime.now()

# def render_graph():
#     global network
#     graph = pydot.Dot("Network", graph_type="graph")
#     for node, conns in network.items():
#         graph.add_node(pydot.Node(node, style='filled'))
#         for c in [c for c in conns if c == min(node, c)]:
#             graph.add_edge(pydot.Edge(node, c, color='red' if (c, node) in [('jqt', 'nvd'), ('bvb', 'cmg'), ('hfx', 'pzl')] else 'black'))
#
#     # graph.write_png("graph.png")
#     graph.write_svg("graph.svg")

def count_partitions(removals):
    global network
    parts = 0
    sizes = []
    rems = { frozenset(c) for c in removals }
    remaining_nodes = set(network.keys())
    while remaining_nodes:
        # sizes.append(0)
        parts += 1
        pnodes = set()
        q = { remaining_nodes.pop() }
        while q:
            node = q.pop()
            pnodes.add(node)
            new_ones = {n for n in network[node] if {n, node} not in rems and n not in pnodes}
            q |= new_ones
            pnodes |= new_ones
        remaining_nodes -= pnodes
        sizes.append(len(pnodes))
    return parts, sizes

network = defaultdict(set)
connections = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        elem, conns = line.split(': ')
        for con in conns.split():
            network[elem].add(con)
            network[con].add(elem)
            connections.append((min(elem, con), max(elem, con)))

# render_graph()

lenc = len(connections)
# FIXME 'xqh' found manually with dot graph
s1 = [(i, c) for i, c in enumerate(connections) if 'xqh' in c]
print(s1)
# for a, b, c in [(a, b, c) for a, b in combinations(connections, 2) for c in s1 if a != c and b != c]:

def run(i, a):
    for j, b in [(j, b) for j, b in enumerate(connections) if j != i]:
        print(i, j, lenc)
        for k, c in [(k, c) for k, c in enumerate(connections[j+1:]) if k != i]:
            parts, sizes = count_partitions((a, b, c))
            if parts == 2:
                print(sizes, reduce(lambda a, b: a*b, sizes), a, b, c)
                print(datetime.datetime.now() - begin_time)
                exit(0)

def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for i, a in s1:
        # for i, a in enumerate(connections):
            executor.submit(run, i, a)

if __name__ == '__main__':
    main()

print(datetime.datetime.now() - begin_time)
