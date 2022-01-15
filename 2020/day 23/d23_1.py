import datetime
from collections import deque
begin_time = datetime.datetime.now()

def move(cups):
    minCup, maxCup = min(cups), max(cups)
    curCup = cups[0]
    # rotate current cup to end of list
    cups.rotate(-1)
    # remove selected cups from this dequeue
    selectedCups = tuple([cups.popleft() for i in range(3)])

    destCup = curCup - 1
    while destCup in selectedCups or destCup < minCup:
        destCup -= 1
        if destCup < minCup:
            destCup = maxCup

    # determine position of destination cup
    pos = cups.index(destCup) + 1
    # rotate to right most position
    cups.rotate(-pos)
    # therefore append selected cups to the left
    cups.extendleft(selectedCups[::-1])
    # rotate dequeue so that next current cup is leftmost
    cups.rotate(pos)

    return cups


def play(moves, cups):
    for i in range(moves):
        cups = move(cups)

    pos = cups.index(1)
    cups.rotate(-pos)
    cups.popleft()
    return ''.join(map(str, cups))

# input, maxMoves = "389125467", 10   # test
input, maxMoves = "284573961", 100
print(play(maxMoves, deque(map(int, input))))
print(datetime.datetime.now() - begin_time)
