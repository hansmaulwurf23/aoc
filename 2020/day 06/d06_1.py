ans = 0
curGroupReadings = ""
with open('./input.txt') as file:
    while line := file.readline():
        if line.rstrip() == '':
            ans += len(set(curGroupReadings))
            curGroupReadings = ""

        curGroupReadings += line.rstrip()

ans += len(set(curGroupReadings))
print(ans)
