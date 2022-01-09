import datetime
import math

begin_time = datetime.datetime.now()

validRanges = {}
validTickets = []
myTicket = []
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
        if not line.startswith('your ticket'):
            myTicket = [int(v) for v in line.split(',')]

    while line := file.readline().rstrip():
        if not line.startswith('nearby tickets'):
            values = [int(v) for v in line.split(',')]
            if not getInvalids(values):
                validTickets.append(values)

mappedFields = []
fieldMapping = {i: list(validRanges.keys()) for i in range(0, len(myTicket))}
for ticket in validTickets:
    for i, value in enumerate(ticket):
        removals = []
        for fieldName in fieldMapping[i]:
            atLeastOneValid = False
            for validRange in validRanges[fieldName]:
                if value in validRange:
                    atLeastOneValid = True

            if not atLeastOneValid:
                removals.append(fieldName)

        for r in removals:
            fieldMapping[i].remove(r)

        newFoundMappings = []
        if len(fieldMapping[i]) == 1 and fieldMapping[i][0] not in mappedFields:
            newFoundMappings.append(i)

        while len(newFoundMappings) > 0:
            i = newFoundMappings.pop(0)
            mappedField = fieldMapping[i][0]
            mappedFields.append(mappedField)
            for j in [j for j in fieldMapping.keys() if i != j]:
                if mappedField in fieldMapping[j]:
                    fieldMapping[j].remove(fieldMapping[i][0])
                    if len(fieldMapping[j]) == 1:
                        newFoundMappings.append(j)

ans = 1
for i in [x for x, v in fieldMapping.items() if v[0].startswith('departure')]:
    ans *= myTicket[i]
print(ans)
print(datetime.datetime.now() - begin_time)
