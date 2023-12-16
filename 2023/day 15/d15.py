import datetime
from functools import reduce
begin_time = datetime.datetime.now()

def calc_hash(content: str):
    return reduce(lambda h, e: (h + ord(e)) * 17 % 256, content, 0)

line = open('./input.txt').readline().rstrip()
p1 = sum([calc_hash(p) for p in line.split(",")])
print(f'part 1: {p1}')
assert p1 in [519603, 1320]

boxes = [list() for _ in range(256)]
for step in line.split(','):
    if step[-1] == '-':
        lbl = step[:-1]
        idx = calc_hash(lbl)
        found = False
        for l, v in boxes[idx]:
            if l == lbl:
                found = [l, v]
        if found:
            le = len(boxes[idx])
            boxes[idx].remove(found)
            assert len(boxes[idx]) == le - 1
    else:
        lbl, f = step.split('=')
        idx = calc_hash(lbl)
        for i, (l, v) in enumerate(boxes[idx]):
            if l == lbl:
                if v != str(f):
                    boxes[idx][i][1] = int(f)
                break
        else:
            boxes[idx].append([lbl, int(f)])

p2 = sum([bi * li * f for bi, lenses in enumerate(boxes, 1) for li, (_, f) in enumerate(lenses, 1)])
print(f'part 2: {p2}')
assert p2 in [244342, 145]
print(datetime.datetime.now() - begin_time)
