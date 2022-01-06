import datetime

begin_time = datetime.datetime.now()
numbers = []
invalid = 756008079
invalidIdx = 631

with open('./input.txt') as file:
    while line := file.readline().rstrip():
        numbers.append(int(line))

i = 0
j = 0
curSum = numbers[i]
while j < invalidIdx:
    if curSum < invalid:
        j += 1
        curSum += numbers[j]
    elif curSum > invalid:
        curSum -= numbers[i]
        i += 1
    else:
        break

print(f'invalid number {invalid} can be summed by index {i} to {j}')
print(f'{min(numbers[i:j+1]) + max(numbers[i:j+1])}')

print(datetime.datetime.now() - begin_time)
