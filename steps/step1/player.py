class Player:
    """Player implementation for the step 1.

    :param id: unique identifier for the player. (Default None)
    :param score: score of the player. (Default 0)
    """

    def __init__(self, id=None, score=0):
        self.id = id
        self.score = score

    def __lt__(self, other):
        return self.score < other.score

    def __eq__(self, other):
        return self.socre == other.score

    def __str__(self):
        return "ID: {0}, Score: {1}".format(self.id, self.score)
