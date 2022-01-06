import datetime
begin_time = datetime.datetime.now()

grid = []
with open('./input.txt') as file:
    while line := file.readline().rstrip():
        grid.append(list(line))

def printGrid():
    for row in grid:
        for t in row:
            print(t, end='')
        print('')


def inGrid(x, y):
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)


def adjacents(x, y):
    res = []
    for m, n in [(i+x, j+y) for i in range(-1, 2) for j in range(-1, 2)]:
        if inGrid(m, n) and (m, n) != (x, y):
            res.append((m, n))
    return res


def step():
    switches = []
    for (x, y) in [(x, y) for y in range(len(grid)) for x in range(len(grid[y]))]:
        if grid[y][x] == '.':
            continue

        noOcc = [grid[n][m] for (m, n) in adjacents(x, y)].count('#')
        if grid[y][x] == '#' and noOcc >= 4:
            switches.append([x, y])
        elif grid[y][x] == 'L' and noOcc == 0:
            switches.append([x, y])

    for (x, y) in switches:
        grid[y][x] = '#' if grid[y][x] == 'L' else 'L'

    # printGrid()
    # print('===================================================')
    return len(switches)

changes = 1
while(changes):
    changes = step()
    print(f'changes: {changes}')

occupados = 0
for row in grid:
    occupados += len([x for x in row if x == '#'])

print(occupados)
print(datetime.datetime.now() - begin_time)
