import datetime

begin_time = datetime.datetime.now()

grid = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        grid.append(list(map(int, line)))

scenic = 0
for x in range(1, len(grid[0]) - 1):
    for y in range(1, len(grid) - 1):
        v = grid[y][x]
        left, right, top, bottom = 0, 0, 0, 0

        _x = x - 1
        while _x >= 0 and grid[y][_x] < v:
            _x -= 1
            left += 1
        left += 1 if _x >= 0 else 0

        _x = x + 1
        while _x < len(grid[y]) and grid[y][_x] < v:
            _x += 1
            right += 1
        right += 1 if _x < len(grid[y]) else 0

        _y = y - 1
        while _y >= 0 and grid[_y][x] < v:
            _y -= 1
            top += 1
        top += 1 if _y >= 0 else 0

        _y = y + 1
        while _y < len(grid) and grid[_y][x] < v:
            _y += 1
            bottom += 1
        bottom += 1 if _y < len(grid) else 0

        if (s := (left * right * top * bottom)) > scenic:
            scenic = s

print(scenic)
print(datetime.datetime.now() - begin_time)
