import curses
from .base import *

class Menu(Widget):
    def __init__(self, coord, texts, title=True, center=True):
        super().__init__(coord)
        self.texts = list(texts)
        if center:
            max_length = len(max(texts, key=len))
            for i in range(len(texts)):
                nb_space = int(max_length / 2 - len(texts[i]) / 2)
                self.texts[i] = " " * nb_space + texts[i]
                self.texts[i] = self.texts[i] + (max_length - len(self.texts[i])) * " "

        self.title = title
        self.select = 1 if self.title else 0
        self.function = lambda x : None


    def _go_up(self):
        if self.select == (1 if self.title else 0):
            self.select = len(self.texts) - 1
        else:
            self.select -= 1

    def _go_down(self):
        if self.select == len(self.texts) - 1:
            self.select = 1 if self.title else 0
        else:
            self.select += 1

    def bind(self, f):
        self.function = f

    def draw(self, app):
        super().draw(app)
        for i in range(len(self.texts)):
            if i == self.select:
                app.stdscr.addstr(self.coord[0] + i, self.coord[1], self.texts[i], curses.A_STANDOUT)
            else:
                app.stdscr.addstr(self.coord[0] + i, self.coord[1], self.texts[i])

    def update(self, app):
        c = app.stdscr.getch()
        if c == curses.KEY_UP:
            self._go_up()
        if c == curses.KEY_DOWN:
            self._go_down()
        if c in (curses.KEY_ENTER, 10 ,13):
            return self.function(self.select)
        if c == 27:
            return False
        return True

    def start(self, app):
        self.draw(app)
        while self.update(app):
            app.stdscr.clear()
            app.stdscr.refresh()
            self.draw(app)
