import curses
import sys
from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, wrapper
from aopython import vector_add

class MapView(object):

    DIRS = {KEY_UP: (0, -1), KEY_DOWN: (0, 1), KEY_LEFT: (-1, 0), KEY_RIGHT: (1, 0)}
    YOFF, XOFF = 3, 4

    def __init__(self, filename, stdscr):
        self.stdscr = stdscr
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.pos = [0, 0]
        self.DIMX = len(self.lines[0])
        self.DIMY = len(self.lines)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.curs_set(0)
        self.update_map()
        self.curses_control()

    def in_map(self, x, y):
        return 0 <= x < self.DIMX and 0 <= y < self.DIMY

    def draw_x_axis(self):
        for x in range(0, self.DIMX, 1):
            self.draw_x_tick(x)

    def draw_x_tick(self, x, atts = None):
        atts = curses.color_pair(1) if atts is None else atts
        self.stdscr.addstr(1, self.XOFF + x, str(x % 10), atts)
        if x >= 10:
            self.stdscr.addstr(0, self.XOFF + x, str(x // 10), atts)

    def draw_y_axis(self):
        for y in range(0, self.DIMY, 1):
            self.draw_y_tick(y)

    def draw_y_tick(self, y, atts = None):
        atts = curses.color_pair(1) if atts is None else atts
        self.stdscr.addstr(self.YOFF + y, 0, str(y).rjust(self.XOFF-1), atts)

    def draw_lines(self):
        for y, line in enumerate(self.lines):
            self.stdscr.addstr(y + self.YOFF, self.XOFF, ''.join(line))

    def set_highlight(self, newpos = None, oldpos = None):
        if oldpos is not None:
            x, y = oldpos
            self.stdscr.addch(y + self.YOFF, x + self.XOFF, self.lines[y][x], curses.color_pair(1))
            self.draw_y_tick(y)
            self.draw_x_tick(x)

        x, y = (self.pos if newpos is None else newpos)
        self.stdscr.addch(y + self.YOFF, x + self.XOFF, self.lines[y][x], curses.color_pair(2))
        self.draw_y_tick(y, curses.color_pair(2))
        self.draw_x_tick(x, curses.color_pair(2))

        self.stdscr.refresh()

    def update_pos(self):
        pstr = str(self.pos).ljust(10)
        self.stdscr.addstr(self.DIMY + self.YOFF + 1, self.DIMX + self.XOFF + 1, pstr)
        self.stdscr.refresh()

    def update_map(self):
        self.draw_x_axis()
        self.draw_y_axis()
        self.draw_lines()
        self.set_highlight()
        self.update_pos()
        self.stdscr.refresh()

    def curses_control(self):
        global pos
        c = self.stdscr.getch()
        while c != ord('q'):
            if c in self.DIRS.keys():
                nxt = vector_add(self.pos, self.DIRS[c])
                if self.in_map(*nxt):
                    self.set_highlight(nxt, self.pos)
                    self.pos = nxt
                    self.update_pos()
            c = self.stdscr.getch()

def main(stdscr):
    if len(sys.argv) < 1:
        print(f"> python3 mapview.py <ascii_file>")
        exit(-1)
    else:
        MapView(sys.argv[1], stdscr)

if __name__ == '__main__':
    wrapper(main)

