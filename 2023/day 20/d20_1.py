import datetime
from collections import deque, defaultdict

from aopython import dotdict, vector_add

begin_time = datetime.datetime.now()

LO, HI = range(2)
INV = [HI, LO]
BRDCSTR = 'broadcaster'
FLPFLP = '%'
CONJ = '&'
OUTPUT = 'output'

def run_signal():
    global modules
    counter = [0, 0]
    comm = deque([(BRDCSTR, LO, 'button')])

    while comm:
        mod, sgnl, src = comm.popleft()
        # print(f'{src} -{"high" if sgnl else "low"}-> {mod}')
        counter[sgnl] += 1

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

    return counter

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

counter = [0, 0]
for _ in range(1000):
    res = run_signal()
    counter = vector_add(res, counter)

p1 = (counter[0] * counter[1])
print(f'part 1: {p1}')
assert p1 in [839775244, 32000000, 11687500]

print(datetime.datetime.now() - begin_time)
