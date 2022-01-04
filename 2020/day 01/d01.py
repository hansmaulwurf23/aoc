numbersByLastDigit = [[] for i in range(10)]

with open('./input.txt') as file:
    while line := file.readline().rstrip():
        numbersByLastDigit[int(line) % 10].append(int(line))

for (i, j, k) in [(i,j,k) for i in range(10) for j in range(10) for k in range(10)]:
    if (i + j + k) % 10 == 0:
        for a in numbersByLastDigit[i]:
            for b in numbersByLastDigit[j]:
                for c in numbersByLastDigit[k]:
                    if a + b + c == 2020:
                        print(a*b*c)
                        exit(0)