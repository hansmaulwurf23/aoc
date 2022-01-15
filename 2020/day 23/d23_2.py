import datetime
begin_time = datetime.datetime.now()

def cups_tostring(curCup, cups):
    result = f'({curCup}) '
    i = curCup
    while cups[i] != curCup:
        result += f'{cups[i]} '
        i = cups[i]

    return result


def move(cups, curCup, minCup, maxCup):
    selectedCups = [0] * 3
    curIdx = curCup

    # selected removal
    for i in range(3):
        selectedCups[i] = cups[curIdx]
        curIdx = cups[curIdx]

    cups[curCup] = cups[selectedCups[-1]]

    destCup = curCup - 1
    while destCup in selectedCups or destCup < minCup:
        destCup -= 1
        if destCup < minCup:
            destCup = maxCup

    cups[selectedCups[-1]] = cups[destCup]
    cups[destCup] = selectedCups[0]

    return cups[curCup]


def play(moves, cups, curCup, minCup, maxCup):
    for i in range(moves):
        if i % 1000000 == 0:
            print(i)
        curCup = move(cups, curCup, minCup, maxCup)

    print(f'{cups[1]} - {cups[cups[1]]}')
    return cups[1], cups[cups[1]]


def create_linked_list(input, entries):
    result = [0] * (len(input) + 1)
    listInput = list(map(int, input))
    for prev, next in zip(listInput, listInput[1:]):
        result[prev] = next

    if len(input) < maxEntries:
        maxInput = max(listInput)
        result[listInput[-1]] = maxInput + 1
        result += list(range(maxInput + 2, entries + 2))
        result[-1] = listInput[0]
        maxCup = entries
    else:
        result[listInput[-1]] = listInput[0]
        maxCup = max(listInput)

    return result, min(listInput), maxCup


# input = "389125467"
input = "284573961"
# maxMoves = 10
maxMoves = 10000000
# maxEntries = 9
maxEntries = 1000000
linked_list, minCup, maxCup = create_linked_list(input, maxEntries)
a, b = play(maxMoves, linked_list, int(input[0]), minCup, maxCup)
print(a*b)
print(datetime.datetime.now() - begin_time)
