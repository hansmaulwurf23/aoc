import re

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
    if validKeySet - curRecord.keys():
        continue
    if not (1920 <= int(curRecord['byr']) <= 2002):
        # print(f'{curRecord["byr"]} byr wrong')
        continue
    if not (2010 <= int(curRecord['iyr']) <= 2020):
        # print(f'{curRecord["iyr"]} iyr wrong')
        continue
    if not (2020 <= int(curRecord['eyr']) <= 2030):
        # print(f'{curRecord["eyr"]} eyr wrong')
        continue
    if not (curRecord['hgt'].endswith(('cm', 'in'))):
        # print(f'{curRecord["hgt"]} hgt wrong')
        continue
    elif curRecord['hgt'].endswith('cm') and not (150 <= int(curRecord['hgt'].replace('cm', '')) <= 193):
        # print(f'{curRecord["hgt"]} hgt wrong')
        continue
    elif curRecord['hgt'].endswith('in') and not (59 <= int(curRecord['hgt'].replace('in', '')) <= 76):
        # print(f'{curRecord["hgt"]} hgt wrong')
        continue
    if not re.match(r'^#[0-9a-f]{6}$', curRecord['hcl']):
        print(f'{curRecord["hcl"]} hcl did not match')
        continue
    if not curRecord['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        # print(f'{curRecord["ecl"]} ecl wrong')
        continue
    if not re.match(r'^\d{9}$', curRecord['pid']):
        # print(f'{curRecord["pid"]} pid wrong')
        continue

    print(f'{[f"{k}:{curRecord[k]}".rjust(9, " ") for k in sorted(curRecord) if k != "cid"]} passed')
    validRecords += 1

print(validRecords)
