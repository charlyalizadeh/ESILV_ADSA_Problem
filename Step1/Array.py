from Player import Player

class Array:
    def __init__(self, size=0):
        self.size = size
        self._array = [Player(i, 0) for i in range(self.size)]

    def delete_last(self, n=10):
        """Reduce the value of self.size.

        :param int n: The number of which is strip from `self.size`
        """

        self.size -= n

    def set_values(self, values):
        """Set the values of the array to values.

        :param iterable values: New values of the array.
        """

        for i in range(self.size):
            self._array[i] = values[i]
            if i >= len(values):
                break

    def sort(self, alg="merge"):
        """Sort the array with the specified algorithm.

        :param str alg: A string representing the sort algorithm.
        """

        if alg == "merge":
            print("merge")
            self._array = sorted(self._array)
        elif alg == "couting":
            self._array = self.counting_sort(self._array)

    def counting_sort(self, array):
        """Return an list sorted with couting sort algorithm.

        :param iterable array: Iterable which is sorted.
        :return: Sorted list version of `array`.
        :rtype: list
        """

        max_node = max(self._array)
        count = [0] * (max_node.value + 1)
        for node in array:
            count[node.value] += 1
        total = 0
        for i in range(max_node.value + 1):
            count[i], total = total, count[i] + total

        output = [0] * len(self._array)
        for node in self._array:
            output[count[node.value]] = node
            count[node.value] += 1
        return output

    def display_cli(self):
        """Display the array in the console."""

        for node in self._array:
            print(node.value, end = '-')
        print()
