import datetime

from showgrid import show_grid

begin_time = datetime.datetime.now()

dots = set()
folds = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        x, y = map(int, line.split(','))
        dots.add((x, y))

    while line := f.readline().rstrip():
        dim, val = line.replace('fold along ', '').split('=')
        folds.append((dim, int(val)))

for i, (dim, v) in enumerate(folds):
    result = set()
    d = 0 if dim == 'x' else 1
    for dot in dots:
        if dot[d] > v:
            newd = [*dot]
            newd[d] = 2 * v - newd[d]
            result.add(tuple(newd))
        else:
            result.add(dot)
    dots = result
    if i == 0:
        print(f'part 1: {len(dots)}')

show_grid(dots, s=750, fh=5, fw=35, invert_yaxis=True)
print(datetime.datetime.now() - begin_time)
