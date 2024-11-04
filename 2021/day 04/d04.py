import copy
import datetime
from collections import Counter

begin_time = datetime.datetime.now()


def in_board(board_idx, number):
    global checked, boards
    board = boards[board_idx]
    for y, row in enumerate(board):
        for x, val in enumerate(row):
            if val == number:
                checked[board_idx].append((x, y))
                return True


def check_win(board_idx):
    global checked, boards
    checks = checked[board_idx]
    for dim in range(2):
        if (c := Counter(map(lambda x: x[dim], checks))).most_common(1)[0][1] == 5:
            return True


def calc_score(board_idx):
    global checked, boards
    bc = copy.deepcopy(boards[board_idx])
    for x, y in checked[board_idx]:
        bc[y][x] = 0
    return sum([sum(row) for row in bc])


with open('./input.txt') as f:
    lines = f.read().splitlines()

numbers = list(map(int, lines[0].split(',')))
boards = [[]]
checked = [[]]

for l in lines[2:]:
    if not l:
        boards.append([])
        checked.append([])
        continue
    boards[-1].append([int(x) for x in l.split()])

winners = dict()
for n in numbers:
    for bi in range(len(boards)):
        if bi not in winners and in_board(bi, n) and check_win(bi):
            winners[bi] = n * calc_score(bi)

winorder = list(winners)
print(f'part 1: {winners[winorder[0]]}')
print(f'part 2: {winners[winorder[-1]]}')
print(datetime.datetime.now() - begin_time)
