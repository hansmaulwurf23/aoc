corrects = 0

with open('./input.txt') as file:
    while line := file.readline().rstrip():
        conf, passw = line.split(': ')
        fromTo, char = conf.split(' ')
        i, j = [int(x) - 1 for x in fromTo.split('-')]
        if (passw[i] == char) != (passw[j] == char):
            # print(f'{i} {j} {char} {passw}')
            corrects += 1

print(corrects)