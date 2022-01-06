import datetime

begin_time = datetime.datetime.now()
numbers = []
preambel = []

preambelSize = 25
with open('./input.txt') as file:
    while line := file.readline().rstrip():
        numbers.append(int(line))

preambel = numbers[0:preambelSize]


def isValid(n):
    for (i, j) in [(i, j) for i in range(preambelSize) for j in range(preambelSize) if i < j]:
        # print(f'{preambel[i]} + {preambel[j]} = {preambel[i] + preambel[j]} =? {n}')
        if preambel[i] + preambel[j] == n:
            return True
    return False


for i in range(preambelSize, len(numbers)):
    if isValid(numbers[i]):
        preambel.pop(0)
        preambel.append(numbers[i])
    else:
        break

print(f'not valid index {i} number: {numbers[i]}')

print(datetime.datetime.now() - begin_time)
