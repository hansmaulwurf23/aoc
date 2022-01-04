hill = []

with open('./input.txt') as file:
    while line := file.readline().rstrip():
        hill.append(line[::1])

treeCounter = 0
result = 1

for (dx, dy) in [[1,1], [3,1], [5,1], [7,1], [1,2]]:
    (x, y) = [0, 0]
    treeCounter = 0
    while y < len(hill):
        if hill[y][(x % len(hill[y]))] == '#':
            treeCounter += 1
        (x, y) = [x + dx, y + dy]

    result *= treeCounter

print(result)
