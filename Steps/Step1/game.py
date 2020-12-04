from .avltree import AVLTree
from .array import Array
import random

class Game:
    def __init__(self, datastructure="Array", nb_players=100):
        self.nb_players = nb_players
        self.datastructure = datastructure
        if self.datastructure == "Array":
            self.players = Array(nb_players)
        else:
            self.players = AVLTree(nb_players)
        self.round = 0

    def delete_last_player(self, n=10):
        """Delete the n last player from the game.

        :param int n: The number of player to delete.
        """

        self.players.delete_last(n)

    def sort_players(self):
        """Sort the players by their score.

        Apply the correct algorithm in function of the chosen data structure.
        We couldn't do one interface for both datastructure because for the AVLTree
        we need to create a new instance of AVLTree. This may change in the future.
        """

        if self.datastructure == "Array":
            self._sort_players_Array()
        elif self.datastructure == "AVLTree":
            self._sort_players_AVLTree()

    def _sort_players_Array(self):
        """Sort the players by their score considering the data structure being an Array."""

        self.players.sort()

    def _sort_players_AVLTree(self):
        """Sort the players by their score considering the data structure being an AVLTree."""

        new_players = AVLTree()
        self.players.copy_nodes(new_players)
        self.players = new_players

    def generate_random_score(self):
        """Generate random finale scores of an Among Us game.

        Generate random scores. For now the scores are not feasible with the rules.

        :return: A list of interger representing the scores of the playes.
        :rtype: list of int.
        """

        return random.choices(range(13), k=10)

    def simulate_game(self, rand=False):
        """Simulate game.

        :param bool rand: Boolean which indicates whether the game are created randomly or based on the score.
        """

        nb_team = int(self.players.nb_player/10)
        scores = []
        for i in range(nb_team):
            scores.extend(self._generate_random_score())
        if rand:
            random.shuffle(scores)
        self.players.add_values(scores)
        self.round += 1

    def reinitilize(self, nb_players=None):
        if nb_players is None:
            nb_players = self.nb_players
        if self.datastructure == "Array":
            self.players = Array(nb_players)
        else:
            self.players = AVLTree(nb_players)
        self.log = []
