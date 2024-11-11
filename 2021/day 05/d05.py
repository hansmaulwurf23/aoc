import datetime
from collections import defaultdict

begin_time = datetime.datetime.now()
lines = [defaultdict(list), defaultdict(list)]
diags = [[], []]  # 0 = \ and 1 = /
inters = set()

def get_intersections(dim, start, end, lvl):
    global lines
    intersections = set()
    odim = (dim + 1) % 2

    # intersections of paralells
    for sect in lines[dim][lvl]:
        sf, st = sect
        fi, ti = max(start, sf), min(end, st)

        if fi <= ti:
            for di in range(fi, ti + 1):
                el = [lvl, lvl]
                el[dim] = di
                intersections.add(tuple(el))

    # crossings
    for olvl, sects in {l: s for l, s in lines[odim].items() if start <= l <= end}.items():
        for sf, st in [(f, t) for f, t in sects if f <= lvl <= t]:
            el = [lvl, lvl]
            el[dim] = olvl
            intersections.add(tuple(el))

    return intersections


def diag_intersetions(ori, idx):
    fx, fy, tx, ty = diags[ori][idx]


with open('./input.txt') as file:
    while line := file.readline().rstrip():
        fx,fy,tx,ty = map(int, line.replace(' -> ',',').split(','))

        if fx != tx and fy != ty:
            if fx > tx:
                fx, tx, fy, ty = tx, fx, ty, fy
            diags[0 if fy < ty else 1].append((fx, fy, tx, ty))
        else:
            fx, tx = list(sorted([fx, tx]))
            fy, ty = list(sorted([fy, ty]))
            dim, f, t, lvl = (0, fx, tx, fy) if fy == ty else (1, fy, ty, fx)
            inters |= get_intersections(dim, f, t, lvl)
            lines[dim][lvl].append((f, t))

print(f'{len(inters)}')
print(datetime.datetime.now() - begin_time)
