import datetime

begin_time = datetime.datetime.now()

grid = []
with open('./input.txt') as f:
    while line := f.readline().rstrip():
        grid.append(list(map(int, line)))

visible = 2 * len(grid) + 2 * (len(grid[0]) - 2)
for x in range(1, len(grid[0]) - 1):
    for y in range(1, len(grid) - 1):
        v = grid[y][x]

        if max(grid[y][0:x]) < v or \
           max(grid[y][x+1:]) < v or \
           max(list(grid[t][x] for t in range(0, y))) < v or \
           max(list(grid[t][x] for t in range(y + 1, len(grid)))) < v:
            visible += 1

print(visible)
print(datetime.datetime.now() - begin_time)
