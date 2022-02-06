import datetime
import showgrid
from aopython import min_max_2d, vector_add
from intcode import IntCodeMachine

begin_time = datetime.datetime.now()

NORTH, SOUTH, WEST, EAST = map(ord, ['^', 'v', '<', '>'])
moves = { NORTH: (0, -1), SOUTH: (0, 1), EAST: (+1, 0), WEST: (-1, 0) }
turns = { NORTH: { WEST: 'L', EAST: 'R' },
          SOUTH: { EAST: 'L', WEST: 'R' },
          EAST: { NORTH: 'L', SOUTH: 'R' },
          WEST: { NORTH: 'R', SOUTH: 'L'}}
SCAFFOLD = 35


def read_testmap():
    coords = []
    with open('./testmap.txt') as f:
        y = 0
        while line := f.readline().rstrip():
            for x, c in enumerate(line):
                if c == '#':
                    coords.append((x, y))
                elif ord(c) in moves.keys():
                    coords.append((x, y))
                    robot = (x, y)
                    start_dir = ord(c)
            y += 1

    return coords, robot, start_dir


def adjacents(pos):
    for m in moves.values():
        yield tuple(vector_add(pos, m))


def get_scaffold(output):
    scaffold = set()
    x, y = 0, 0
    for o in output:
        if o == 10:
            x = 0
            y += 1
        else:
            if o == 35:
                scaffold.add((x, y))
            elif o in moves.keys():
                scaffold.add((x, y))
                robot = (x, y)
                start_dir = o
            x += 1

    return scaffold, robot, start_dir


def get_intersections(scaffolds):
    intersections = set()
    for s in scaffolds:
        if len(list(filter(lambda x: x in scaffolds, adjacents(s)))) == 4:
            intersections.add(s)
    return intersections


def follow_scaffold(scaffolds, pos, dir):
    cmds = []

    while True:
        for turn in turns[dir].keys():
            if tuple(vector_add(pos, moves[turn])) in scaffolds:
                newdir = turn
                delta = moves[turn]
                break

        if newdir == dir:
            print(f'end at {pos}')
            break

        cmds.append(turns[dir][newdir])
        pos = vector_add(pos, delta)
        steps = 1
        while True:
            newpos = tuple(vector_add(pos, delta))
            if newpos not in scaffolds:
                break
            else:
                steps += 1
                pos = newpos

        cmds.append(str(steps))
        dir = newdir

    return cmds


def find_repeating_codes(cmds, split_cmds, movement_funcs):
    if len(movement_funcs) >= 3:
        return

    oneline = ','.join(cmds)
    # print(f'[{len(used_commands)}] inspecting {oneline}')

    # movement function can only be 20 characters long -> 10 commands + comma best case
    for l in range(min(10, len(cmds)), 3, -1):

        # search for repeating patterns
        for p in range(0, len(cmds) - l + 1):
            test = ','.join(cmds[p:p + l])

            # in case pattern had two digit lengths i.e. L11
            if len(test) > 20:
                continue

            # with no found movement functions the test pattern should appear at least three times
            if (counter := oneline.count(test)) > 2 or len(movement_funcs) > 0:

                # get rest of cmds after test pattern "applied"
                leftovers = []
                for leftover in split_cmds:
                    leftovers.extend(list(map(lambda x: x.strip(',').split(','), filter(None, ','.join(leftover).split(test)))))

                # print(f'[{len(movement_funcs)}] {test} -> {counter} ({len(test)}) REST: {leftovers}')
                if not leftovers:
                    movement_funcs.append(test)
                    print(movement_funcs)
                    return movement_funcs
                elif len(movement_funcs) >= 3:
                    continue
                elif len(leftovers) + len(movement_funcs) > 10:
                    continue

                for r in leftovers:
                    if len(r) > 3:
                        new_mvmt_funcs = movement_funcs.copy()
                        new_mvmt_funcs.append(test)
                        res = find_repeating_codes(list(r), leftovers, new_mvmt_funcs)
                        if res is not None:
                            return res


def calc_main_func(oneline_cmds, movement_funcs):
    main_func = oneline_cmds
    for i, m in enumerate(movement_funcs):
        main_func = main_func.replace(m, ['A', 'B', 'C'][i])

    return main_func


with open('./input.txt') as f:
    program = [int(x) for x in f.readlines()[0].split(',')]

vm = IntCodeMachine(program)
output = vm.run([])
scaffold, robot, start_dir = get_scaffold(output)
intersections = get_intersections(scaffold)
cmds = follow_scaffold(scaffold, robot, start_dir)
# showgrid.show_grid(scaffolds, intersections)


# scaffold, robot, start_dir = read_testmap()
# cmds = follow_scaffold(scaffold, robot, start_dir)
# print(','.join(cmds))
# cmds = 'R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2'.split(',')

oneline = ','.join(map(str, cmds))
print(oneline)
print(f'commas: {oneline.count(",")} length: {len(oneline)}')
codes = find_repeating_codes(cmds, [cmds], [])
main_func = calc_main_func(oneline, codes)
print(main_func)
print(len(main_func))

# now suck it robot
program[0] = 2
vm.reset(program)
input = []
for c in main_func:
    input.append(ord(c))
input.append(10)

for mf in codes:
    for c in mf:
        input.append(ord(c))
    input.append(10)

input.append(ord('n'))
input.append(10)

outs = vm.run(input)
print(outs[-1])
print(datetime.datetime.now() - begin_time)
