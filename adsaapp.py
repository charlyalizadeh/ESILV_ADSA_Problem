from interface import *
from steps import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from copy import copy


class ADSAApp():
    """The class managing the interface for the project.

    :param App app: The curses app wrapper where we will draw the interface.
    """

    def __init__(self, app=None):
        if app is None:
            app = App()
        self.app = app
        height, width = self.app.stdscr.getmaxyx()
        self.widgets = {}

        # Main Menu
        texts_main_menu = ["Choose a step:", "Step 1", "Step 2", "Step 3", "Step 4", "Exit"]
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
            #self.display_step4()
            self.step4()
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
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.expand_frame_repr', False)

        names = ["Reactor", "UpperE", "LowerE", "Security", "Electrical",
                 "Medbay", "Storage", "Cafetaria", "Unnamed1", "Unnamed2",
                 "O2", "Weapons", "Shield", "Navigations"]
        graph_crewmates = Graph(0)
        graph_crewmates.import_from_file(filepath_crewmates)
        distances = graph_crewmates.floydWarshall()
        df_crewmates = pd.DataFrame(data=distances, index=names, columns=names)
        lines = df_crewmates.__str__().split("\n")
        screen_game.insert_line("CREWMATES")
        for line in lines:
            screen_game.insert_line(line)

        names = ["Reactor", "UpperE", "LowerE", "Security", "Electrical",
                 "Medbay", "Storage", "Cafetaria", "Unnamed1", "Unnamed2",
                 "O2", "Weapons", "Shield", "Navigations", "CorridorW"]
        graph_impostors = Graph(0)
        graph_impostors.import_from_file(filepath_impostors)
        distances = graph_impostors.floydWarshall()
        df_impostors = pd.DataFrame(data=distances, index=names, columns=names)
        lines = df_impostors.__str__().split("\n")
        screen_game.insert_line("")
        screen_game.insert_line("IMPOSTORS")
        for line in lines:
            screen_game.insert_line(line)
        screen_game.start(self.app)

    def step4(self):
        step4app = Step4App(self.app)
        step4app.start()

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


class Step4App():
    def __init__(self, app=None, adjmatrix_path="data/graph_crewmates.txt", pos_path="data/coordinates.txt"):
        if app is None:
            app = App()
        self.app = app
        height, width = self.app.stdscr.getmaxyx()
        self.widgets = {}
        self.graph = Graph(0)
        self.graph.import_from_file(adjmatrix_path)
        self.pos_path = pos_path

        self.src_vertex = range(self.graph.nb_vertex)
        self.dst_vertex = range(self.graph.nb_vertex)

        # Main Menu
        texts_main_menu = ["Choose an option for finding a Hamilton path:",
                           "Minimum between all path",
                           "Minium at a specific source vertex",
                           "Minimum at a specific destination vertex",
                           "Minium at a specific source and destination vertices",
                           "Exit"]
        main_menu = Menu(self._get_coord_centered(height, width, texts_main_menu),
                         texts_main_menu,
                         True,
                         True)
        main_menu.bind(lambda choice : self.main_menu(choice))
        self.widgets["main_menu"] = main_menu

        # Source vertex menu
        texts_menu_src_vertex = ["Choose a source vertex:"]
        texts_menu_src_vertex.extend(self.graph.label)
        texts_menu_src_vertex.append("All")
        menu_src_vertex = Menu(self._get_coord_centered(height, width, texts_menu_src_vertex),
                               texts_menu_src_vertex,
                               True,
                               True)
        menu_src_vertex.bind(lambda choice: self.menu_src_vertex(choice))
        self.widgets["menu_src_vertex"] = menu_src_vertex

        # Destination vertex menu
        texts_menu_dst_vertex = ["Choose an destination vertex:"]
        texts_menu_dst_vertex.extend(self.graph.label)
        texts_menu_dst_vertex.append("All")
        menu_dst_vertex = Menu(self._get_coord_centered(height, width, texts_menu_dst_vertex),
                               texts_menu_dst_vertex,
                               True,
                               True)
        menu_dst_vertex.bind(lambda choice: self.menu_dst_vertex(choice))
        self.widgets["menu_dst_vertex"] = menu_dst_vertex

    def main_menu(self, choice):
        if choice == 1:
            self.min_hamilton_path()
        if choice == 2:
            self.app.stdscr.clear()
            self.widgets["menu_src_vertex"].start(self.app)
            self.min_hamilton_path()
        if choice == 3:
            self.app.stdscr.clear()
            self.widgets["menu_dst_vertex"].start(self.app)
            self.min_hamilton_path()
        if choice == 4:
            self.app.stdscr.clear()
            self.widgets["menu_src_vertex"].start(self.app)
            self.widgets["menu_dst_vertex"].start(self.app)
            self.min_hamilton_path()

    def min_hamilton_path(self, src_vertex=None, dst_vertex=None):
        self.app.stdscr.clear()
        if src_vertex is None:
            src_vertex = self.src_vertex
        if dst_vertex is None:
            dst_vertex = self.dst_vertex

        graph = self.graph
        paths = graph.get_hamilton_path(src_vertex, dst_vertex)
        height, width = self.app.stdscr.getmaxyx()
        screen_game = FakeScreen([5, 5], [height - 10, width - 10])
        screen_game.insert_line(f"Graph with {graph.nb_vertex} vertices and {graph.nb_edge} edges.")
        screen_game.insert_line(f"Starting vertex index: {src_vertex}")
        screen_game.insert_line(f"Starting vertex label: {[self.graph.label[i] for i in src_vertex]}")
        screen_game.insert_line(f"Ending vertex index: {dst_vertex}")
        screen_game.insert_line(f"Ending vertex label: {[self.graph.label[i] for i in dst_vertex]}")
        if not paths:
            screen_game.insert_line("")
            screen_game.insert_line("No Hamilton paths")
            screen_game.insert_line("Press the escape key to continue...")
            screen_game.start(self.app)
        else:
            screen_game.insert_line("")
            screen_game.insert_line(f"{len(paths)} hamilton paths found.")
            shortest_path, min_weight = graph.get_shortest_path(paths)
            screen_game.insert_line(f"Shortest path index -> {shortest_path}")
            screen_game.insert_line(f"Shortest path label -> {[self.graph.label[i] for i in shortest_path]}")
            screen_game.insert_line(f"Min weight -> {min_weight}")
            screen_game.insert_line("")
            screen_game.insert_line("Press the escape key to display the shortest path...")
            screen_game.start(self.app)
            graph.set_path(shortest_path)
            graph.plot(filepos=self.pos_path)
            plt.show()

    def menu_src_vertex(self, choice):
        if choice == self.graph.nb_vertex + 1:
            self.src_vertex = range(self.graph.nb_vertex)
        else:
            self.src_vertex = [choice - 1]

    def menu_dst_vertex(self, choice):
        if choice == self.graph.nb_vertex + 1:
            self.dst_vertex = range(self.graph.nb_vertex)
        else:
            self.dst_vertex = [choice - 1]

    def _get_coord_centered(self, height, width, texts):
        max_length = len(max(texts, key=len))
        y = int(height / 2 - len(texts) / 2)
        x = int(width / 2 - max_length / 2)
        return y, x

    def start(self):
        self.widgets["main_menu"].start(self.app)
