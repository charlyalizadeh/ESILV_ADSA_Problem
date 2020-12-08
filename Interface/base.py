import curses
import uuid
import os


class App:
    def __init__(self, unicode_support=False):
        os.environ.setdefault('ESCDELAY', '0')
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(True)
        self.windows = {}
        self.order = []
        self.deactivated_windows = []
        self.unicode_support = False

    def __del__(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()




class Widget:
    def __init__(self, coord = [0, 0], id=None):
        self.coord = coord

    def draw(self, app):
        height, width = app.stdscr.getmaxyx()
        app.stdscr.addstr(height - 1, 0, "Copyright: © Alizadeh Charly, Juliette Barthet")

    def update(self, app):
        pass

    def start(self, app):
        pass

