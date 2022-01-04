corrects = 0

with open('./input.txt') as file:
    while line := file.readline().rstrip():
        conf, passw = line.split(': ')
        fromTo, char = conf.split(' ')
        min, max = [int(x) for x in fromTo.split('-')]
        if passw[::1].count(char) in range(min, max+1):
            # print(f'{min} {max} {char} {passw}')
            corrects += 1

print(corrects)