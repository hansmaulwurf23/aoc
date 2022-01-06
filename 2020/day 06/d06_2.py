ans = 0
curGroupReadings = set()
firstReading = True
with open('./input.txt') as file:
    while line := file.readline():
        if line.rstrip() == '':
            ans += len(curGroupReadings)
            firstReading = True
            continue

        if firstReading:
            firstReading = False
            curGroupReadings = set(line.rstrip())
        else:
            curGroupReadings = curGroupReadings.intersection(set(line.rstrip()))

ans += len(set(curGroupReadings))
print(ans)
