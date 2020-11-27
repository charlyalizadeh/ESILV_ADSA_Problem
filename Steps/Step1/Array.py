from .Player import Player

class Array:
    def __init__(self, size=0):
        self.size = size
        self._array = [Player(i, 0) for i in range(self.size)]

    def delete_last(self, n=10):
        """Reduce the value of self.size.

        :param int n: The number of which is strip from `self.size`
        """

        self.size -= n

    def add_values(self, values):
        """Set the values of the array to values.

        :param iterable values: New values of the array.
        """

        for i in range(self.size):
            if i >= len(values):
                break
            self._array[i].score += values[i]

    def sort(self, alg="merge"):
        """Sort the array with the specified algorithm.

        :param str alg: A string representing the sort algorithm.
        """

        if alg == "merge":
            self._array = sorted(self._array, reverse=True)
        elif alg == "couting":
            self._array = self.counting_sort(self._array)

    def counting_sort(self, array):
        """Return an list sorted with couting sort algorithm.

        :param iterable array: Iterable which is sorted.
        :return: Sorted list version of `array`.
        :rtype: list
        """

        max_node = max(self._array)
        count = [0] * (max_node.score + 1)
        for node in array:
            count[node.score] += 1
        total = 0
        for i in range(max_node.score, -1, -1):
            count[i], total = total, count[i] + total

        output = [0] * len(self._array)
        for node in self._array:
            output[count[node.score]] = node
            count[node.score] += 1
        return output

    def display_cli(self):
        """Display the array in the console."""

        for node in self._array:
            print(node.value, end = '-')
        print()

    def __getattr__(self, key):
        if key == "nb_player":
            return self.size

    def __iter__(self):
        return self._array.__iter__()

    def __next__(self):
        return self._array.__next__()

    def __str__(self):
        descrition = ""
        index = 0
        print(self.size)
        for node in self._array:
            descrition += node.__str__() + "\n"
            index += 1
            if index == self.size:
                break
        return descrition
