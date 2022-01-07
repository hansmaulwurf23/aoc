import datetime

begin_time = datetime.datetime.now()
busOffsets = {}
busRemainders = {}

with open('./input.txt') as file:
    lines = file.readlines()
    ts = int(lines[0])
    for i, x in enumerate([x for x in lines[1].split(',')]):
        if x != 'x':
            busOffsets[int(x)] = i

for busID, offset in busOffsets.items():
    offset = busID - offset
    while offset < 0:
        offset += busID

    busRemainders[busID] = offset % busID

maxBusID = max(busRemainders.keys())
maxBusIDOffset = busRemainders[maxBusID]
busIDRunMatches = {}

print(busOffsets)
print(busRemainders)

t = maxBusIDOffset
run = 0
factor = 1
while True:
    remainderOffsetSum = 0
    # print(str(t).ljust(10), end='-> ')
    for busID, remainder in busRemainders.items():
        r = abs(t % busID - remainder)
        if r == 0 and busID != maxBusID:
            # new bus ID in current loop steps
            if busID not in busIDRunMatches.keys():
                busIDRunMatches[busID] = []
                factor *= busID
                print(f'{str(busID).rjust(5)} {str(run).rjust(5)} {str((t - maxBusIDOffset) / maxBusID).ljust(10)}')
            busIDRunMatches[busID].append(run)
        # print(f'{str(busID).rjust(4)}: {str(r).rjust(4)}', end=' ')
        remainderOffsetSum += r

    if remainderOffsetSum == 0:
        break

    # print('')
    t += (maxBusID * factor)
    run += 1

print(t)
print(datetime.datetime.now() - begin_time)
