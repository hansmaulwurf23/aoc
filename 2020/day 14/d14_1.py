import datetime
begin_time = datetime.datetime.now()

mem = {}
andMask = 0
orMask = 0

with open('./input.txt') as file:
    while line := file.readline().rstrip():
        if line[0:4] == 'mask':
            readMask = line[7:]
            andMask = int("".join(['0' if b == '0' else '1' for b in list(readMask)]), 2)
            orMask  = int("".join(['1' if b == '1' else '0' for b in list(readMask)]), 2)
        else:
            (memAddr, val) = line.split(' = ')
            val = int(val)
            memAddr = int(memAddr.replace('mem[', '').replace(']', ''))
            mem[memAddr] = (val & andMask) | orMask

print(sum(list(mem.values())))
print(datetime.datetime.now() - begin_time)
