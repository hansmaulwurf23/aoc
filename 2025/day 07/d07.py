import datetime
from collections import defaultdict
begin_time = datetime.datetime.now()

FREE, SPLITTER = '.', '^'
grid = []

def part1(start_idx):
    beams, splits = {start_idx}, 0
    cur_lvl = 1

    while cur_lvl < len(grid):
        newb = set()
        for b in beams:
            if grid[cur_lvl][b] == SPLITTER:
                splits += 1
                newb |= {b - 1, b + 1}
            else:
                newb.add(b)
        cur_lvl += 1
        beams = newb

    return splits

def part2(start_idx):
    beams = {start_idx: 1}
    cur_lvl = 1

    while cur_lvl < len(grid):
        newb = defaultdict(int)
        for b, counter in beams.items():
            if grid[cur_lvl][b] == SPLITTER:
                newb[b + 1] += counter
                newb[b - 1] += counter
            else:
                newb[b] += counter
        cur_lvl += 1
        beams = newb

    return sum(beams.values())

with open('./input.txt') as f:
    while line := f.readline().rstrip():
        grid.append(line)

start_idx = grid[0].index('S')
print(f'Part 1: {part1(start_idx)}')
print(f'Part 2: {part2(start_idx)}')
print(datetime.datetime.now() - begin_time)
