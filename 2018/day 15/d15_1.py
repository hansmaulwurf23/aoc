import datetime
import heapq
import math
import os
from collections import namedtuple, defaultdict, deque

import imageio as imageio

import showgrid
from aopython import vector_add, min_max_2d

begin_time = datetime.datetime.now()

Unit = namedtuple('Unit', ['HP', 'AP'])
elves = dict()
goblins = dict()
walls = set()
MAKE_GIF = False
SHOW_PLT = False
GIF_DIR = '/tmp/d15/'


def init_gif():
    if not os.path.exists(GIF_DIR):
        os.mkdir(GIF_DIR)


def gif_frame(frame_no):
    if MAKE_GIF or SHOW_PLT:
        plt = showgrid.show_grid(walls, {'r': elves.keys(), 'darkgreen': goblins.keys()}, c='grey',
                                 s=240, highlightsize=160, no_show=(not SHOW_PLT))
        if not MAKE_GIF:
            return
        plt.savefig(f'{GIF_DIR}{str(frame_no).rjust(4, "0")}.png')
        plt.close()


def save_gif():
    if MAKE_GIF:
        if os.path.exists(f'{GIF_DIR}battle.gif'):
            os.remove(f'{GIF_DIR}battle.gif')
        with imageio.get_writer(f'{GIF_DIR}battle.gif', mode='I') as writer:
            for f in sorted(os.listdir(GIF_DIR)):
                if not f.endswith(".png"):
                    continue
                image = imageio.imread(os.path.join(GIF_DIR, f))
                writer.append_data(image)
                os.remove(os.path.join(GIF_DIR, f))


def output_raw(round):
    if round == 0:
        f = open("./myout.txt", "w")
    else:
        f = open("./myout.txt", "a")

    fx, tx, fy, ty = min_max_2d(walls)
    unit_infos = []
    for u in elves.keys():
        heapq.heappush(unit_infos, ((u[1], u[0]), elves[u].HP))
    for u in goblins.keys():
        heapq.heappush(unit_infos, ((u[1], u[0]), goblins[u].HP))

    f.write(f'Round: {round}\n\n')

    for y in range(fy, ty + 1):
        for x in range(fx, tx + 1):
            c = '.'
            if (x, y) in walls:
                c = '#'
            elif (x, y) in elves:
                c = 'E'
            elif (x, y) in goblins:
                c = 'G'
            f.write(c)
        if unit_infos:
            uinfo = heapq.heappop(unit_infos)
            f.write(f'   {str(uinfo[0][0]).ljust(2)}   {str(uinfo[0][1]).ljust(2)}   {str(uinfo[1])}\n')
        else:
            f.write('\n')

    f.write('\n')
    f.close()


def is_adjacent(a, b):
    ax, ay = a
    bx, by = b
    return (ax == bx and (ay + 1 == by or ay - 1 == by)) or \
           (ay == by and (ax + 1 == bx or ax - 1 == bx))


def adjacents(pos, only_free_space=False):
    res = []
    for m in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
        x, y = tuple(vector_add(pos, m))
        if only_free_space and ((x, y) in elves or (x, y) in goblins):
            continue
        if (x, y) not in walls:
            res.append((x, y))

    return res


def nearest_target(root, targets):
    q = deque()
    visited = set()
    visited.add(root)
    q.appendleft((root, 0, None))
    found = []
    min_distance = math.inf
    while q:
        node, steps, first_step = q.pop()

        if node in targets and min_distance >= steps:
            found.append((node, steps, first_step))
            min_distance = steps
            continue

        # cannot be better?
        if min_distance <= steps:
            continue

        for a in adjacents(node):
            if (a in elves or a in goblins) and a not in targets:
                continue
            if a not in visited:
                visited.add(a)
                q.appendleft((a, steps + 1, first_step if first_step is not None else a))

    if found:
        target, steps, first_step = min(found, key=lambda f: (f[0][1], f[0][0], f[2][1], f[2][0]))
        return target, steps, first_step
    else:
        return None, None, None


def unit_turn(u, allies, targets):
    target = None
    # key = adjacent of target / value = set of target
    possible_moves = defaultdict(set)
    for t in sorted(targets.keys(), key=lambda t: (t[1], t[0])):
        if is_adjacent(u, t) and (target is None or targets[target].HP > targets[t].HP):
            target = t
        if target:
            continue
        for a in adjacents(t, only_free_space=True):
            possible_moves[a].add(t)

    # no target is immediately adjacent -> move move ya!
    if not target and possible_moves:
        move_target, steps, new_pos = nearest_target(u, possible_moves.keys())
        if move_target is None:
            # cannot move and have no target -> my turn is done
            return

        allies[new_pos] = allies[u]
        del allies[u]
        u = new_pos
        # did unit move onto adjacent position of target(s)?
        if u in possible_moves:
            target = min(possible_moves[u], key=lambda t: targets[t].HP)

    if target:
        targets[target] = Unit(HP=targets[target].HP - allies[u].AP, AP=targets[target].AP)
        if targets[target].HP <= 0:
            del targets[target]


def combat_round():
    # all unit coordinates in reading order
    unit_coords = sorted(list(elves.keys()) + list(goblins.keys()), key=lambda t: (t[1], t[0]))
    for u in unit_coords:
        allies, targets = (elves, goblins) if u in elves else (goblins, elves)
        if u not in allies:
            # unit could have died in a previous battle in this round
            continue
        if not allies or not targets:
            return False
        unit_turn(u, allies, targets)

    return True


with open('./input.txt') as f:
    y = 0
    while line := f.readline().rstrip():
        for x, c in enumerate(line):
            if c == '#':
                walls.add((x, y))
            elif c == 'G':
                goblins[(x, y)] = Unit(HP=200, AP=3)
            elif c == 'E':
                elves[(x, y)] = Unit(HP=200, AP=3)

        y += 1

rounds = 0
init_gif()
gif_frame(rounds)
# output_raw(rounds)
while True:
    last_winner_score = max([sum(map(lambda u: u.HP, team.values())) for team in [elves, goblins]])
    # print(rounds * last_winner_score, rounds)
    full_round = combat_round()
    gif_frame(rounds)
    if full_round:
        rounds += 1
    else:
        break
    # output_raw(rounds)

save_gif()
winner = elves if elves else goblins
print(rounds * sum(map(lambda w: w.HP, winner.values())), rounds)
print(datetime.datetime.now() - begin_time)
