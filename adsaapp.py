from interface import *
from steps import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class ADSAApp():
    """The class managing the interface for the project. Not the cleanest code I wrote but it does the work and nothing else.

    :param App app: The curses app wrapper where we will draw the interface.
    """

    def __init__(self, app = None):
        if app is None:
            app = App()
        self.app = app
        height, width = self.app.stdscr.getmaxyx()
        self.widgets = {}

        # Main Menu
        texts_main_menu = [ "Choose a step:", "Step 1", "Step 2", "Step 3", "Step 4", "Exit"]
        main_menu = Menu(self._get_coord_centered(height, width, texts_main_menu), texts_main_menu, True, True)
        main_menu.bind(lambda x : self.main_menu_function(x))
        self.widgets["main_menu"] = main_menu

        # Step1 Menu
        texts_step1 = [ "Wich datastructure do you want to use ?", "AVL Tree", "Array", "Return"]
        step1_menu = Menu(self._get_coord_centered(height, width, texts_step1), texts_step1, True, True)
        step1_menu.bind(lambda x : self.step1_menu_function(x))
        self.widgets["step1_menu"] = step1_menu

    def main_menu_function(self, index):
        self.app.stdscr.clear()
        if index == 1:
            self.widgets["step1_menu"].start(self.app)
        elif index == 2:
            self._find_impostors("data/adjacency_matrix.txt")
        elif index == 3:
            self._get_distance("data/graph_crewmates.txt", "data/graph_impostors.txt")
        elif index == 4:
            self.display_step4()
        elif index == 5:
            return False
        return True

    def step1_menu_function(self, index):
        self.app.stdscr.clear()
        game = None
        if index == 1:
            self._play_game("AVLTree")
        elif index == 2:
            self._play_game("Array")
        return False

    def _play_game(self, datastructure):
        height, width = self.app.stdscr.getmaxyx()
        screen_game = FakeScreen([5, 5], [height - 10, width - 10])
        game = Game(datastructure)
        screen_game.insert_line(f"Game created with {datastructure} to store the players.")
        for i in range(3):
            screen_game.insert_line(f"Playing round {game.round}.")
            screen_game.insert_line(f"  ↪Remaining players {game.get_nb_players()}.")
            game.simulate_game()

        game.sort_players()
        screen_game.insert_line(f"END POOL !")
        while game.get_nb_players() > 10:
            screen_game.insert_line(f"Playing round {game.round}")
            screen_game.insert_line(f"  ↪Remaining players {game.get_nb_players()}.")
            game.simulate_game(True)
            game.sort_players()
            game.delete_last_player()

        screen_game.insert_line(f"FINALS:")
        for i in range(5):
            screen_game.insert_line(f"Playing round {game.round}")
            screen_game.insert_line(f"  ↪Remaining players {game.get_nb_players()}.")
            game.simulate_game(True)
            game.sort_players()
        
        last_players = game.players.__str__().split('\n')
        if datastructure == "AVLTree":
            last_players = last_players[::-1]
        for i in range(len(last_players)):
            screen_game.insert_line(f"{i + 1}. {last_players[i]}")
        screen_game.start(self.app)

    def _find_impostors(self, filepath):
        height, width = self.app.stdscr.getmaxyx()
        screen_game = FakeScreen([5, 5], [height - 10, width - 10])
        adjacency_matrix = np.genfromtxt(filepath, delimiter=",")
        suspects = get_suspects(adjacency_matrix, [0])
        screen_game.insert_line("Suspects:")
        for key, val in suspects.items():
            screen_game.insert_line(f"  {key} is a suspect. He met {val} dead player.")
        suspects_pair = get_suspects_pairs(suspects, adjacency_matrix, [0])
        screen_game.insert_line("")
        screen_game.insert_line("Suspects pair:")
        for pair in suspects_pair:
            screen_game.insert_line(f"  {pair[0]} and {pair[1]}")
        screen_game.insert_line("")
        screen_game.insert_line("Press the escape key to continue...")
        screen_game.start(self.app)

    def _get_distance(self, filepath_crewmates, filepath_impostors, position=None):
        height, width = self.app.stdscr.getmaxyx()
        screen_game = FakeScreen([5, 5], [height - 10, width - 10])
        names = ["Reactor", "UpperE", "LowerE", "Security", "Electrical", "Medbay", "Storage", "Cafetaria", "Unnamed1", "Unnamed2", "O2", "Weapons", "Sield", "Navigations"]
        graph = Graph(0)
        graph.import_from_file(filepath_crewmates)
        distances = graph.floydWarshall()
        df_crewmates = pd.DataFrame(data=distances, index = names, columns = names)
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        lines = df_crewmates.__str__().split("\n")
        for l in lines:
            screen_game.insert_line(l)
        screen_game.start(self.app)

    def display_step4(self, adjmatrix_path="data/graph_crewmates.txt", pos_path="data/coordinates.txt"):
        graph = Graph(0)
        graph.import_from_file(adjmatrix_path)
        paths = graph.get_all_hamilton_path()
        height, width = self.app.stdscr.getmaxyx()
        screen_game = FakeScreen([5, 5], [height - 10, width - 10])
        screen_game.insert_line(f"Graph with {graph.nb_vertex} vertices and {graph.nb_edge} edges.")
        screen_game.insert_line(f"This graph contains {len(paths)} hamilton paths.")
        shortest_path = graph.get_shortest_path(paths)
        screen_game.insert_line(f"Shortest path -> {shortest_path}")
        screen_game.insert_line("Press the escape key to display the shortest path...")
        screen_game.start(self.app)

        graph.set_path(shortest_path)
        graph.plot(filepos=pos_path)
        plt.show()

    def _get_coord_centered(self, height, width, texts):
        max_length = len(max(texts, key=len))
        y = int(height / 2 - len(texts) / 2)
        x = int(width / 2 - max_length / 2)
        return y, x

    def start(self):
        self.widgets["main_menu"].start(self.app)
