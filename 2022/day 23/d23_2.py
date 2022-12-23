import datetime
import os
from collections import defaultdict
import imageio as imageio
import showgrid
from aopython import vector_add

begin_time = datetime.datetime.now()

#  7 0 1
#  6 X 2
#  5 4 3
N, NE, E, SE, S, SW, W, NW = range(8)
MOVES = {N: (0, 1), NE: (1, 1), E: (1, 0), SE: (1, -1), S: (0, -1), SW: (-1, -1), W: (-1, 0), NW: (-1, 1)}
# hard coding this? yes, because fiddle this fuck in code is not readable thats why
CHECK_PRIO = [((N, NW, NE), (S, SE, SW), (W, NW, SW), (E, NE, SE)),
              ((S, SE, SW), (W, NW, SW), (E, NE, SE), (N, NW, NE)),
              ((W, NW, SW), (E, NE, SE), (N, NW, NE), (S, SE, SW)),
              ((E, NE, SE), (N, NW, NE), (S, SE, SW), (W, NW, SW))]

elves, no_elves, cur_prio = set(), None, 0
MAKE_GIF, SHOW_PLT, GIF_DIR = False, False, '/tmp/d23/'


def init_gif():
    if not os.path.exists(GIF_DIR):
        os.mkdir(GIF_DIR)


def gif_frame(frame_no, moved_elves, stationary_elves):
    if MAKE_GIF or SHOW_PLT:
        plt = showgrid.show_grid(stationary_elves, highlights=moved_elves, s=6, highlightsize=6, fh=6, fw=6,
                                 no_show=(not SHOW_PLT), xrange=[-15, 125], yrange=[-125, 15], title=f'frame={frame_no}')
        if not MAKE_GIF:
            return
        plt.savefig(f'{GIF_DIR}{str(frame_no).rjust(4, "0")}.png')
        plt.close()


def save_gif():
    if MAKE_GIF:
        if os.path.exists(f'{GIF_DIR}moves.gif'):
            os.remove(f'{GIF_DIR}moves.gif')
        with imageio.get_writer(f'{GIF_DIR}moves.gif', mode='I') as writer:
            for f in sorted(os.listdir(GIF_DIR)):
                if not f.endswith(".png"):
                    continue
                image = imageio.imread(os.path.join(GIF_DIR, f))
                writer.append_data(image)
                os.remove(os.path.join(GIF_DIR, f))


def round(elves, cur_prio):
    prop_moves = defaultdict(list)

    for e in elves:
        moved = False
        free_dirs = [tuple(vector_add(e, MOVES[d])) not in elves for d in range(len(MOVES))]
        if all(free_dirs):
            prop_moves[e].append(e)
            continue
        for checks in CHECK_PRIO[cur_prio]:
            direction = checks[0]
            if all(free_dirs[check] for check in checks):
                np = tuple(vector_add(e, MOVES[direction]))
                prop_moves[np].append(e)
                moved = True
                break
        if not moved:
            # is that even right?
            prop_moves[e].append(e)

    moved_elves = set()
    stationary_elves = set()
    for np, movers in prop_moves.items():
        if len(movers) == 1:
            if np != movers[0]:
                moved_elves.add(np)
            else:
                stationary_elves.add(np)
        else:
            moved_elves |= set(movers)

    return moved_elves, stationary_elves


def calc_free_ground(elves):
    minx, maxx, miny, maxy = [None] * 4
    for ex, ey in elves:
        if minx is None or ex < minx: minx = ex
        if maxx is None or ex > maxx: maxx = ex
        if miny is None or ey < miny: miny = ey
        if maxy is None or ey > maxy: maxy = ey

    print(f'x {minx} {maxx} y {miny} {maxy}')
    return (maxx - minx + 1) * (maxy - miny + 1) - no_elves


with open('./input.txt') as f:
    y = 0
    while line := f.readline().rstrip():
        for x, c in enumerate(line):
            if c == '#':
                elves.add((x, y))
        y -= 1

    no_elves = len(elves)


init_gif()
gif_frame(0, elves, set())
r = 1
while True:
    moved_elves, stationary_elves = round(elves, cur_prio)
    gif_frame(r, moved_elves, stationary_elves)
    if not moved_elves:
        break
    r += 1
    elves = moved_elves | stationary_elves
    cur_prio = (cur_prio + 1) % len(CHECK_PRIO)

save_gif()
calc_free_ground(elves)
print(r)
print(datetime.datetime.now() - begin_time)

