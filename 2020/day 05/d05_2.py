existingVals = []
with open('./input.txt') as file:
    while line := file.readline().rstrip():
        existingVals.append(int(line.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1'), 2))

ans = -1
oldVal = -1
for i in sorted(existingVals):
    if oldVal != -1 and (i - oldVal) > 1:
        print(f'{oldVal} - {i}')
        ans = oldVal + 1
    oldVal = i


print(ans)