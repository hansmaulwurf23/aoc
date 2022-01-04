hill = []

with open('./input.txt') as file:
    while line := file.readline().rstrip():
        hill.append(line[::1])

(x, y) = [0, 0]
(dx, dy) = [3, 1]
treeCounter = 0

def checkTree(x, y):
    if (hill[y][(x % len(hill[y]))] == '#'):
        return 1
    else:
        return 0

while y < len(hill):
    treeCounter += checkTree(x, y)
    (x, y) = [x + dx, y + dy]

print(treeCounter)
