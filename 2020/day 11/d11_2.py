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


def countOccupados(x, y):
    occs = 0
    (width, height) = (len(grid[0]), len(grid))

    # northwest \
    (_x, _y) = (x - 1, y - 1)
    while _x >= 0 and _y >= 0 and grid[_y][_x] == '.':
        (_x, _y) = (_x - 1, _y - 1)
    if inGrid(_x, _y) and grid[_y][_x] == '#': occs += 1

    # northeast /
    (_x, _y) = (x + 1, y - 1)
    while _x < width and _y >= 0 and grid[_y][_x] == '.':
        (_x, _y) = (_x + 1, _y - 1)
    if inGrid(_x, _y) and grid[_y][_x] == '#': occs += 1

    # southwest /
    (_x, _y) = (x - 1, y + 1)
    while _x >= 0 and _y < height and grid[_y][_x] == '.':
        (_x, _y) = (_x - 1, _y + 1)
    if inGrid(_x, _y) and grid[_y][_x] == '#': occs += 1

    # southeast \
    (_x, _y) = (x + 1, y + 1)
    while _x < width and _y < height and grid[_y][_x] == '.':
        (_x, _y) = (_x + 1, _y + 1)
    if inGrid(_x, _y) and grid[_y][_x] == '#': occs += 1

    # west -
    (_x, _y) = (x - 1, y)
    while _x >= 0 and grid[_y][_x] == '.':
        _x = _x - 1
    if inGrid(_x, _y) and grid[_y][_x] == '#': occs += 1

    # east -
    (_x, _y) = (x + 1, y)
    while _x < width and grid[_y][_x] == '.':
        _x = _x + 1
    if inGrid(_x, _y) and grid[_y][_x] == '#': occs += 1

    # north |
    (_x, _y) = (x, y - 1)
    while _y >= 0 and grid[_y][_x] == '.':
        _y = _y - 1
    if inGrid(_x, _y) and grid[_y][_x] == '#': occs += 1

    # south |
    (_x, _y) = (x, y + 1)
    while _y < height and grid[_y][_x] == '.':
        _y = _y + 1
    if inGrid(_x, _y) and grid[_y][_x] == '#': occs += 1

    return occs


def step():
    switches = []
    for (x, y) in [(x, y) for y in range(len(grid)) for x in range(len(grid[y]))]:
        if grid[y][x] == '.':
            continue

        noOcc = countOccupados(x, y)
        if grid[y][x] == '#' and noOcc >= 5:
            switches.append([x, y])
        elif grid[y][x] == 'L' and noOcc == 0:
            switches.append([x, y])

    for (x, y) in switches:
        grid[y][x] = '#' if grid[y][x] == 'L' else 'L'

    # printGrid()
    print('===================================================')
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
