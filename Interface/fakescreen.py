import curses
from .base import *

class FakeScreen(Widget):
    def __init__(self, coord, dim):
        super().__init__(coord)
        self.dim = dim
        self.lines = []
        self.offsets = [0, 0]
        self.longest_string = 0

    def _draw_border(self, app):
        for i in range(self.coord[0], self.coord[0] + self.dim[0] + 1):
            app.stdscr.addstr(i, self.coord[1], " ", curses.A_STANDOUT)
            app.stdscr.addstr(i, self.coord[1] + self.dim[1], " ", curses.A_STANDOUT)

        for i in range(self.coord[1], self.coord[1] + self.dim[1] + 1):
            app.stdscr.addstr(self.coord[0], i, " ", curses.A_STANDOUT)
            app.stdscr.addstr(self.coord[0] + self.dim[0], i, " ", curses.A_STANDOUT)

    def _draw_lines(self, app):
        for i in range(self.offsets[0], self.offsets[0] + self.dim[0] - 1):
            index = i - self.offsets[0]
            if i >= len(self.lines):
                break
            line = self.lines[i][self.offsets[1]:self.offsets[1] + self.dim[1] - 1]
            app.stdscr.addstr(self.coord[0] + 1 + index, self.coord[1] + 1, line)

    def set_line(index, line):
        if len(line) > self.longest_string:
            self.longest_string = len(line)
        self.lines[index] = line

    def insert_line(self, line):
        if len(line) > self.longest_string:
            self.longest_string = len(line)
        if len(self.lines) >= self.dim[0] - 1:
            self.offsets[0] += 1
        self.lines.append(line)

    def _go_up(self):
        if len(self.lines) - self.offsets[0] >= self.dim[0]:
            self.offsets[0] += 1

    def _go_down(self):
        if self.offsets[0] > 0:
            self.offsets[0] -= 1

    def _go_right(self):
        if self.longest_string - self.offsets[1] > self.dim[1] - 1:
            self.offsets[1] += 1

    def _go_left(self):
        if self.offsets[1] > 0:
            self.offsets[1] -= 1

    def draw(self, app):
        super().draw(app)
        self._draw_border(app)
        self._draw_lines(app)

    def update(self, app):
        c = app.stdscr.getch()
        if c == curses.KEY_DOWN:
            self._go_up()
        elif c == curses.KEY_UP:
            self._go_down()
        elif c == curses.KEY_LEFT:
            self._go_left()
        elif c == curses.KEY_RIGHT:
            self._go_right()
        elif c == 27:
            return False
        return True

    def start(self, app):
        self.draw(app)
        while self.update(app):
            app.stdscr.clear()
            app.stdscr.refresh()
            self.draw(app)

