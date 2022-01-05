validKeySet = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
allKeySet = validKeySet + ['cid']
records = []
curRecord = {}
with open('./input.txt') as file:
    while line := file.readline():
        if line.rstrip() == '':
            records.append(curRecord)
            curRecord = {}
            continue

        for x in line.rstrip().split(' '):
            (k, v) = x.split(':')
            curRecord[k] = v

records.append(curRecord)

validRecords = 0
for curRecord in records:
    if not (validKeySet - curRecord.keys()):
        validRecords += 1

print(validRecords)
