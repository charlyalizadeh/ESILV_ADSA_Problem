def read_coordinates(path):
    """Read two-dimensional coordinates from a file and return them as a nested list.

    :param str path: path to the coordinates file.
    :return:  a iterable containing the coordinates.
    :rtype: a list of list
    """

    file = open(path, "r")
    coordinates = {}
    index = 0
    for line in file.readlines():
        line = line.split(",")
        coordinates[index] = [float(line[0]), -float(line[1])]
        index += 1
    return coordinates
