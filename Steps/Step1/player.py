class Player:
    def __init__(self, id=None, score=0):
        self.id = id
        self.score = score

    def __lt__(self, other):
        """Operator overloading of the lesser than operator.

        :param other: The node which is compared to `self`.
        :return: A boolean value indicating whether `self` is less than `other` or not.
        :rtype: bool
        """

        return self.score < other.score

    def __eq__(self, other):
        """Operator overloading of the equal operator.

        :param other: The node which is compared to `self`.
        :return: A boolean value indicating whether `self` equal than `other` or not.
        :rtype: bool
        """

        return self.socre == other.score

    def __str__(self):
        return "ID: {0}, Score: {1}".format(self.id, self.score)
