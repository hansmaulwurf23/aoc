import datetime
begin_time = datetime.datetime.now()

validRanges = {}
practicalRanges = []
errorRate = 0


def updatePracticalRanges(r):
    if len(practicalRanges) == 0:
        practicalRanges.append(r)
        return

    for x in practicalRanges:
        if min(x) <= min(r) and max(x) >= max(r):
            return

    practicalRanges.append(r)


def mergeOverlappingRanges(pR):
    pR = sorted(pR, key=min)
    i = 0
    while i < len(pR):
        j = i + 1
        while j < len(pR):
            if min(pR[i]) <= min(pR[j]) <= max(pR[i]) <= max(pR[j]):
                pR[i] = range(min(pR[i]), max(pR[j]) + 1)
                pR.remove(pR[j])
            elif min(pR[j]) <= min(pR[i]) <= max(pR[j]) <= max(pR[i]):
                pR[i] = range(min(pR[j]), max(pR[i]) + 1)
                pR.remove(pR[j])
            elif min(pR[i]) <= min(pR[j]) and max(pR[i]) >= max(pR[j]):
                pR.remove(pR[j])
            else:
                j += 1

        i += 1

    return pR


def getInvalids(l):
    for r in practicalRanges:
        l = [x for x in l if x not in r]

    return l


with open('./input.txt') as file:
    while line := file.readline().rstrip():
        (type, ranges) = line.split(': ')
        validRanges[type] = []
        for r in ranges.split(' or '):
            (f, t) = r.split('-')
            r = range(int(f), int(t) + 1)
            validRanges[type].append(r)
            updatePracticalRanges(r)

    practicalRanges = mergeOverlappingRanges(practicalRanges)

    while line := file.readline().rstrip():
        pass

    while line := file.readline().rstrip():
        if line != 'nearby tickets:':
            values = [int(v) for v in line.split(',')]
            errorRate += sum(getInvalids(values))


print(errorRate)
print(datetime.datetime.now() - begin_time)
