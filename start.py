from Steps import *
from Interface import *

class ADSAWindow(Window):
    def __init__(self, app):
        super().__init__(app)
        height, width = self.app.stdscr.getmaxyx()
        menu = Menu((int(height/2), int(width/2)), ("Choose a step:", "Step1", "Step2", "Step3", "Step4"))
        label = Label((height - 1, 0),  "Press escape two time to exit.")
        menu.bind(lambda x : self.start_step(x))
        self.add_widget(label)
        self.add_widget(menu)


    def start():
        super().start()
        height, width = self.app.stdscr.getmaxyx()

    def start_step(self, index):
        self.app.stdscr.clear()
        self.app.stdscr.nodelay(False)
        if index == 1:
            log = start_step1()
        elif index == 2:
            log = start_step2()
        elif index == 3:
            log = start_step3()
        elif index == 4:
            start_step4()
            return None
        for i in range(len(log)):
            self.app.stdscr.addstr(i, 0, log[i])
        height, width = self.app.stdscr.getmaxyx()
        self.app.stdscr.addstr(height - 1, 0, "Press any key to continue.")
        self.app.stdscr.getch()
        self.app.stdscr.clear()
        self.app.stdscr.nodelay(True)






def main():
    input("Please make your terminal full screen. (Press enter to continue)")
    adsa_app = App()
    adsa_window = ADSAWindow(adsa_app) # There is something wrong with this design
                                       #but I only need this code to work in a particular scope so
                                       #I didn't take too much time to think about it.
    adsa_app.start()



if __name__ == "__main__":
    main()
