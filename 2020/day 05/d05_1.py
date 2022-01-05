maxV = 0
with open('./input.txt') as file:
    while line := file.readline().rstrip():
        val = int(line.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1'), 2)
        if val > maxV:
            maxV = val

print(maxV)