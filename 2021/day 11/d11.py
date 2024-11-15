import datetime
from collections import deque
from traceback import print_tb

from aopython import vector_add

begin_time = datetime.datetime.now()
octos = []
DIRS = list((x, y) for x in range(-1, 2) for y in range(-1, 2) if x != 0 or y != 0)

def in_grid(x, y):
    global octos
    return 0 <= x < len(octos[0]) and 0 <= y < len(octos)


def step():
    global octos

    flashers = set()
    for x, y in [(x, y) for x in range(len(octos[0])) for y in range(len(octos))]:
        octos[y][x] += 1
        if octos[y][x] > 9:
            flashers.add((x, y))

    todos = deque(flashers)
    while todos:
        x, y = todos.popleft()
        for tx, ty in [t for t in map(lambda d: vector_add((x, y), d), DIRS) if in_grid(*t)]:
            octos[ty][tx] += 1
            if octos[ty][tx] > 9 and (tx, ty) not in flashers:
                flashers.add((tx, ty))
                todos.append((tx, ty))

    for x, y in flashers:
        octos[y][x] = 0

    return len(flashers)


with open('./input.txt') as f:
    while line := f.readline().rstrip():
        octos.append(list(map(int, line)))

summe = 0
for i in range(1, 101):
    df = step()
    summe += df
    # print(f'{"\n".join(map(lambda x: ''.join(map(str, x)), octos))}')
print(f'part 1: {summe}')

while True:
    i += 1
    if (step() == len(octos) * len(octos[0])):
        print(f'part 2: {i}')
        break

print(datetime.datetime.now() - begin_time)
