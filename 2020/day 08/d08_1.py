prog = []

with open('./input.txt') as file:
    while line := file.readline().rstrip():
        prog.append(line)

visited = []
pc = 0
acc = 0
while pc < len(prog):
    if (pc in visited):
        break

    visited.append(pc)
    (instr, arg) = prog[pc].split(' ')
    if instr == 'jmp':
        pc += int(arg)
    elif instr == 'acc':
        acc += int(arg)
        pc += 1
    else:
        pc += 1

print(acc)