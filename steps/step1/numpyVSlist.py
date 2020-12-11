import numpy as np
import matplotlib.pyplot as plt
import timeit

class NumpyVSList:
    @staticmethod
    def compute(operation):
        """Compute the time of an operation on a numpy array and a core_list.

        :param str operation: The operation to compute.
        :return: Tuple containing the time of the operation on an numpy array and a core list.
        :rtype: tuple of float
        """

        if operation == "init":
            return NumpyVSList.compute_time_init()
        elif operation == "reading":
            return NumpyVSList.compute_time_reading()
        elif operation == "writing":
            return NumpyVSList.compute_time_writing()

    @staticmethod
    def compute_time_init(nb_values=100, repeat=10000):
        """Compare the time of initialization of a numpy array and a core list.

        :param int nb_values: The number of values in the iterables.
        :param int repeat: The number of times we repeat the experiment.
        :return: The time of initialization of the numpy array and the core list.
        :rtype: tuple of float
        """

        time_numpy_array = timeit.timeit("numpy_array = np.array(range({}))".format(nb_values), number=repeat, setup="import numpy as np") / repeat
        time_core_list = timeit.timeit("[i for i in range({})]".format(nb_values), number=repeat) / repeat
        return time_numpy_array, time_core_list

    @staticmethod
    def compute_time_reading(nb_values=100, repeat=10000):
        """Compare the time of reading of a numpy array and a core list.

        :param int nb_values: The number of values in the iterables.
        :param int repeat: The number of times we repeat the experiment.
        :return: The time of reading of the numpy array and the core list.
        :rtype: tuple of float
        """

        numpy_setup = "import numpy as np\nnumpy_array = np.array(range({}))".format(nb_values)
        numpy_test = "for i in numpy_array: pass"
        core_setup = "core_list = [i for i in range({})]".format(nb_values)
        core_test = "for i in core_list: pass"
        time_numpy_array = timeit.timeit(numpy_test, setup=numpy_setup, number=repeat) / repeat
        time_core_list = timeit.timeit(core_test, setup=core_setup, number=repeat) / repeat
        return time_numpy_array, time_core_list

    @staticmethod
    def compute_time_writing(nb_values=100, repeat=10000):
        """Compare the time of writing of a numpy array and a core list.

        :param int nb_values: The number of values in the iterables.
        :param int repeat: The number of times we repeat the experiment.
        :return: The time of writing of the numpy array and the core list.
        :rtype: tuple of float
        """

        numpy_setup = "import numpy as np\nnumpy_array = np.array(range({}))".format(nb_values)
        numpy_test = "for i in range(len(numpy_array)): numpy_array[i] = 1"
        core_setup = "core_list = [i for i in range({})]".format(nb_values)
        core_test = "for i in range(len(core_list)): core_list[i] = 1"
        time_numpy_array = timeit.timeit(numpy_test, setup=numpy_setup, number=repeat) / repeat
        time_core_list = timeit.timeit(core_test, setup=core_setup, number=repeat) / repeat
        return time_numpy_array, time_core_list

    @staticmethod
    def display_compare_init(nb_values=100, repeat=10000):
        """Display the time of initialization of a numpy array and a core list.

        :param int nb_values: The number of values in the iterables.
        :param int repeat: The number of times we repeat the experiment.
        """

        time_numpy_array, time_core_list = NumpyVSList.compute_time_init(nb_values, repeat)
        print("=====RESULT INITIATION=====")
        print("Number of values: {}".format(nb_values))
        print("Number of repeat: {}".format(repeat))
        print("Mean numpy array: {}".format(time_numpy_array))
        print("Mean core list: {}".format(time_core_list))
        print("T_numpy - T_core = {}".format(time_numpy_array - time_core_list))
        print("===========================")

    @staticmethod
    def display_compare_reading(nb_values=100, repeat=10000):
        """Display the time of reading of a core list and a numpy array.

        :param int nb_values: The number of values in the iterables.
        :param int repeat: The number of times we repeat the experiment.
        """

        numpy_setup = "import numpy as np\nnumpy_array = np.array(range({}))".format(nb_values)
        numpy_test = "for i in numpy_array: pass"
        core_setup = "core_list = [i for i in range({})]".format(nb_values)
        core_test = "for i in core_list: pass"
        time_numpy_array, time_core_list = NumpyVSList.compute_time_reading(nb_values, repeat)
        print("=====RESULT READING=====")
        print("Number of values: {}".format(nb_values))
        print("Number of repeat: {}".format(repeat))
        print("Mean numpy array: {}".format(time_numpy_array))
        print("Mean core list: {}".format(time_core_list))
        print("T_numpy - T_core = {}".format(time_numpy_array - time_core_list))
        print("===========================")
        return time_numpy_array, time_core_list

    @staticmethod
    def display_compare_writing(nb_values=100, repeat=10000):
        """Display the time of writing of a core list and a numpy array.

        :param int nb_values: The number of values in the iterables.
        :param int repeat: The number of times we repeat the experiment.
        """

        numpy_setup = "import numpy as np\nnumpy_array = np.array(range({}))".format(nb_values)
        numpy_test = "for i in range(len(numpy_array)): numpy_array[i] = 1"
        core_setup = "core_list = [i for i in range({})]".format(nb_values)
        core_test = "for i in range(len(core_list)): core_list[i] = 1"
        time_numpy_array, time_core_list = NumpyVSList.compute_time_writing(nb_values, repeat)
        print("=====RESULT WRITING=====")
        print("Number of values: {}".format(nb_values))
        print("Number of repeat: {}".format(repeat))
        print("Mean numpy array: {}".format(time_numpy_array))
        print("Mean core list: {}".format(time_core_list))
        print("T_numpy - T_core = {}".format(time_numpy_array - time_core_list))
        print("===========================")
        return time_numpy_array, time_core_list

    @staticmethod
    def compare_all_plot(nb_values=100, repeat=10000):
        """Plot in a bar plot the different mean computation times of different operations on a numpy array and a core list.

        :param int nb_values: The number of values in the iterables NOT IMPLEMENTED.
        :param int repeat: The number of times we repeat the experiment NOT IMPLEMENTED.
        """
        time_numpy_array = {}
        time_core_list = {}
        for operation in ["init", "reading", "writing"]:
            times = NumpyVSList.compute(operation)
            time_numpy_array[operation] = times[0]
            time_core_list[operation] = times[1]
        print(time_numpy_array)
        print(time_core_list)
        plt.bar(time_numpy_array.keys(), time_numpy_array.values())
        plt.bar(time_core_list.keys(), time_core_list.values())
        plt.show()

NumpyVSList.compare_all_plot()


