import datetime
import pydot

begin_time = datetime.datetime.now()

OP1, OP2, OPERATOR = range(3)

GATES = {
'AND' : lambda x, y: x & y,
'OR' : lambda x, y: x | y,
'XOR' : lambda x, y: x ^ y
}

def render_graph(filename='graph.svg'):
    global gates, wires
    graph = pydot.Dot("Network", graph_type="graph")
    colors = {'OR': 'lightgreen', 'XOR': 'orangered', 'AND': 'yellow3'}
    for w in wires:
        graph.add_node(pydot.Node(w, style='filled'))
    for out, val in gates.items():
        if isinstance(val, tuple):
            i1, i2, op = val
            graph.add_node(pydot.Node(out, style='filled', fillcolor=colors[op], shape='square' if out[0] == 'z' else 'circle'))
            graph.add_edge(pydot.Edge(out, i1, color='black'))
            graph.add_edge(pydot.Edge(out, i2, color='black'))
    graph.write_svg(filename)

def resolve(out):
    global gates, wires
    if out in wires:
        return wires[out]
    else:
        i1, i2, op = gates[out]
        if i1 not in wires:
            resolve(i1)
        if i2 not in wires:
            resolve(i2)
        if i1 in wires and i2 in wires:
            val = GATES[op](wires[i1], wires[i2])
            wires[out] = val
            return val


wires = dict()
gates = dict()
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        k, v = line.split(': ')
        wires[k] = int(v)

    zs = []
    while line := f.readline().rstrip():
        i1, op, i2, out = line.replace('-> ', '').split(' ')
        gates[out] = (i1, i2, op)
        if out[0] == 'z':
           zs.append(out)
    maxz = max(zs)
    zs = [None] * (int(maxz[1:]) + 1)

# render_graph('circuit.svg')
while True:
    for idx in [i for i, v in enumerate(zs) if v is None]:
        out = f'z{idx:02}'
        v = resolve(out)
        if v is not None:
            zs[idx]= v
    else:
        break

p1 = int(''.join([str(x) for x in reversed(zs)]), 2)
assert p1 in (52956035802096, 2024)
print(f'part 1: {p1}')

wrongs = set()
zgs = [g for g in gates if g[0] == 'z' and g != maxz]
# all z's must be XORs
wrongs |= set(filter(lambda g: gates[g][OPERATOR] != 'XOR', zgs))

# rest must be full adders as illustrated in README (see var names derived from there)
for zn in zgs:
    i1, i2, op = gates[zn]
    if zn in wrongs:
        continue

    if zn == 'z00':
        if not (i1 in ('x00', 'y00') and i2 in ('x00', 'y00')):
            wrongs.add(zn)
        continue

    idx = f'{int(zn[1:]):02}'
    o1 = gates[i1][OPERATOR]
    o2 = gates[i2][OPERATOR]
    sn, cn1 = None, None

    if o1 == 'XOR':
        if gates[i1][OP1][1:] == gates[i1][OP2][1:] == idx:
            sn = i1
        else:
            wrongs.add(i1)
    elif o1 == 'OR':
        cn1 = i1
    elif zn != 'z01':
        wrongs.add(i1)

    if o2 == 'XOR':
        if sn is not None:
            wrongs.add(i2)
        elif gates[i2][OP1][1:] == gates[i2][OP2][1:] == idx:
            sn = i2
    elif o2 == 'OR':
        cn1 = i2
    elif zn != 'z01':
        wrongs.add(i2)

    if cn1 is not None:
        rn1, tn1, _ = gates[cn1]
        if gates[rn1][OPERATOR] != 'AND':
            wrongs.add(rn1)
        if gates[tn1][OPERATOR] != 'AND':
            wrongs.add(tn1)

p2 = ','.join(sorted(wrongs))
print(f'part 2: {p2}')
assert p2 == 'hnv,hth,kfm,tqr,vmv,z07,z20,z28'
print(datetime.datetime.now() - begin_time)
