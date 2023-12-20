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

def run_signal(start = BRDCSTR, sgnl = LO, src = 'button'):
    global modules
    counter = [0, 0]
    comm = deque([(start, sgnl, src)])

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
        elif mod == 'rx':
            if sgnl == LO:
                return -1
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
        if kind == FLPFLP:
            modules[mod].state = LO
        elif kind == CONJ:
            cons[mod] = dict()

reset_state(cons)

counter = [0, 0]
for _ in range(1000):
    res = run_signal()
    # print(res)
    counter = vector_add(res, counter)

p1 = (counter[0] * counter[1])
print(p1)
assert p1 in [839775244, 32000000, 11687500]






steps = 0
reset_state(cons)
while True:
    steps += 1
    if run_signal(start='ls', src=BRDCSTR) == -1:
        break
    # print(modules['zh'].state.values())
    # if any(modules['zp'].state.values()):
        # print(steps, modules['zp'])
        # print(steps, list(map(lambda x: f'{x[0]} {x[1].state}', [(n, m) for n, m in modules.items() if n in ('hs', 'fn', 'px', 'zx')])))

    if modules['dl'].state['bz']:
        print(steps)
        pass
    # else:
    #     print(-steps)
    # if steps > 1000:
    #     break
    # print(modules['zh'])

print(steps)
print(207787533680413)
print(datetime.datetime.now() - begin_time)
