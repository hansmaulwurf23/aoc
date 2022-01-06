prog = []

with open('./input.txt') as file:
    while line := file.readline().rstrip():
        prog.append(line)


def runProg(pc, acc, visited, skipped):
    looping = False
    while pc < len(prog):
        # print(f'{prog[pc]}')
        if pc in visited:
            looping = True
            break

        visited.append(pc)

        (instr, arg) = prog[pc].split(' ')
        if instr == 'nop':
            pc += 1
        elif instr == 'acc':
            acc += int(arg)
            pc += 1
        elif instr == 'jmp':
            if skipped == -1:
                (_pc, _acc, _looping, _skipped) = runProg(pc + 1, acc, visited.copy(), skipped=pc)
                if _looping == False:
                    return _pc, _acc, _looping, _skipped
            pc += int(arg)

    return pc, acc, looping, skipped


(pc, acc, looping, skipped) = runProg(0, 0, [], -1)
print(f'ran with pc {pc} acc {acc} looping {looping} and skipped {skipped}')
