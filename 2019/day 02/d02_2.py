import datetime
begin_time = datetime.datetime.now()

with open('./input.txt') as f:
    master = [int(x) for x in f.readlines()[0].split(',')]

# run variants
for noun, verb in [(noun, verb) for noun in range(100) for verb in range(100)]:
    numbers = master.copy()
    numbers[1] = noun
    numbers[2] = verb

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

    if numbers[0] == 19690720:
        break

print(noun, verb, (noun * 100 + verb))
print(datetime.datetime.now() - begin_time)
