import datetime

begin_time = datetime.datetime.now()
busIDs = []

with open('./input.txt') as file:
    lines = file.readlines()
    ts = int(lines[0])
    busIDs = [int(x) for x in lines[1].split(',') if x != 'x']

nextDeparts = {x: x - (ts % x) for x in busIDs}
minBusID = min(nextDeparts, key=nextDeparts.get)
print(minBusID * nextDeparts[minBusID])
print(datetime.datetime.now() - begin_time)
