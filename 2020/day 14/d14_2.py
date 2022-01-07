import datetime
begin_time = datetime.datetime.now()

mem = {}
memMask = []


def calcMemAddrs(addr):
    calcedAddrs = []
    todo = [list(addr)]
    while len(todo) > 0:
        t = todo.pop()
        if t.count('X') > 0:
            posX = t.index('X')
            for i in range(0, 2):
                newT = t.copy()
                newT[posX] = str(i)
                todo.append(newT)
        else:
            calcedAddrs.append("".join(t))

    # print(f'calculated {len(calcedAddrs)} new masks.')
    return calcedAddrs


def applyMask(addr, memMask):
    binAddr = list("{0:b}".format(addr).rjust(len(memMask), '0'))
    resultAddr = []
    for bit, mask in zip(binAddr, memMask):
        if mask == '0':
            resultAddr.append(bit)
        elif mask == '1':
            resultAddr.append('1')
        else:
            resultAddr.append('X')

    return "".join(resultAddr)


with open('./input.txt') as file:
    while line := file.readline().rstrip():
        if line[0:4] == 'mask':
            readMask = line[7:]
            memMask = list(readMask)
        else:
            (memAddr, val) = line.split(' = ')
            val = int(val)
            memAddr = int(memAddr.replace('mem[', '').replace(']', ''))
            for addr in calcMemAddrs(applyMask(memAddr, memMask)):
                mem[addr] = val

print(sum(list(mem.values())))
print(datetime.datetime.now() - begin_time)
