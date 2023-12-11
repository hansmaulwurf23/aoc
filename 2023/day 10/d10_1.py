import datetime
from collections import deque
from aopython import vector_add

begin_time = datetime.datetime.now()
NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
DIRS = { NORTH: (0, -1), SOUTH: (0, 1), EAST: (+1, 0), WEST: (-1, 0) }
INVDIRS = { NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
PIPETYPES = { '|': (NORTH, SOUTH),
              '-': (EAST, WEST),
              'L': (NORTH, EAST),
              'J': (NORTH, WEST),
              '7': (SOUTH, WEST),
              'F': (EAST, SOUTH),
              'S': tuple()
}
READABLES = {'F': '┌', '7': '┐', 'L': '└', 'J': '┘', '|': '│', '-': '─'}

def print_grid(grid):
    print('\n'.join([''.join([READABLES[c] if c in READABLES else c for c in row]) for row in grid]))

grid = []
with open('./input.txt') as f:
    for y, l in enumerate(f.read().splitlines()):
        grid.append([])
        for x, c in enumerate(l):
            grid[-1].append(c)
            if c == 'S':
                start = (x, y)


# finding loops
todo_dirs = deque(DIRS)
for heading in range(3):
    loop, pos, start_dir = [start], list(start), heading
    while True:
        x, y = vector_add(pos, DIRS[heading])
        pos = [x, y]
        if INVDIRS[heading] in PIPETYPES[grid[y][x]]:
            loop.append((x, y))
            if grid[y][x] == 'S':
                break
            f, t = PIPETYPES[grid[y][x]]
            heading = f if INVDIRS[heading] == t else t
        else:
            break
    # loop?
    if tuple(pos) == start:
        longest_loop = loop
        end_dir = INVDIRS[heading]
        todo_dirs.remove(end_dir)
        break

print(f'part 1: {len(longest_loop) // 2}')

start_pipe = {v: k for k, v in PIPETYPES.items()}[(start_dir, end_dir)]
# use only two matching pairs (LJ or 7F) to use upper or lower half of unit square
even_odd_separators = ['|', 'L', 'J']
if start_pipe in even_odd_separators:
    even_odd_separators.append('S')
even_odd_separators = set(even_odd_separators)

## NEXT ONE WORKS BUT SLOW (3,4 sec - since all points need lookups in the set) #############################
# all tiles without the longest loop
# todo_tiles = {(x, y) for y in range(len(grid)) for x in range(len(grid[0]))} - set(longest_loop)
# inside_counter = 0
# while todo_tiles:
#     # create maximum size patch
#     inside = True
#     pos = todo_tiles.pop()
#     q = deque([pos])
#     patch = set([pos])
#     while q:
#         pos = q.pop()
#         patch.add(pos)
#
#         adjs = [tuple(vector_add(pos, a)) for a in DIRS.values()]
#         outside = [0 > ax or ax >= len(grid[0]) or ay < 0 or ay >= len(grid) for ax, ay in adjs]
#         if any(outside):
#             inside = False
#
#         for a, out in zip(adjs, outside):
#             if a not in patch and not out and a in todo_tiles:
#                 q.append(a)
#
#     # make sure tile is inside
#     if inside:
#         t, pipe_crossing = patch.pop(), 0
#         tx, ty = t[0], t[1] - 1
#         while ty >= 0:
#             if (tx, ty) in longest_loop and grid[ty][tx] in ('S', '-', 'J', 'L'):
#                 pipe_crossing += 1
#             ty -= 1
#         if pipe_crossing % 2 == 0:
#             inside = False
#         patch.add(t)
#     todo_tiles -= patch
#
#     if inside:
#         inside_counter += len(patch)
#     # print('INSIDE' if inside else 'OUTSIDE', len(patch), patch)
#############################################################################################################

# rebuild grid with longest loop and start only everything else is space
new_grid = []
# sort loop by y and then x to compare only the first in queue
sorted_loop = deque(sorted(longest_loop, key=lambda x: (x[1], x[0])))
for y, row in enumerate(grid):
    new_grid.append([])
    for x, cell in enumerate(row):
        if sorted_loop and (x, y) == sorted_loop[0]:
            new_grid[-1].append(cell)
            sorted_loop.popleft()
        else:
            new_grid[-1].append(' ')
grid = new_grid

# even-odd-coloring
inside_counter = 0
for y, row in enumerate(grid):
    pipe_crossings = 0
    for x, v in enumerate(row):
        # p = READABLES[v] if v in READABLES else v
        if v in even_odd_separators:
            pipe_crossings += 1
        elif v == ' ' and pipe_crossings % 2:
            inside_counter += 1
            # p = 'X'
        # print(p, end='')
    # print('')

print(f'part 2: {inside_counter}')
print(datetime.datetime.now() - begin_time)
