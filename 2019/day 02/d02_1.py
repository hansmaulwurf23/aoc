import datetime
begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    numbers = [int(x) for x in f.readlines()[0].split(',')]

# apply "1202 program alarm" patch
numbers[1] = 12
numbers[2] = 2

# run prog
for pc in range(0, len(numbers), 4):
    if numbers[pc] == 99:
        break

    operands = [numbers[numbers[pc+1]], numbers[numbers[pc+2]]]
    dest_addr = numbers[pc+3]
    if numbers[pc] == 1:
        numbers[dest_addr] = sum(operands)
    elif numbers[pc] == 2:
        numbers[dest_addr] = operands[0] * operands[1]
    else:
        print(f'unknown op code! {numbers[pc]}')
        break


print(numbers[0])
print(datetime.datetime.now() - begin_time)
