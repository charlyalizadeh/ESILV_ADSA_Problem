from .Graph import Graph
import matplotlib.pyplot as plt

def read_coordinates(filename):
    file = open(filename, "r")
    coordinates = {}
    index = 0
    for line in file.readlines():
        line = line.split(",")
        coordinates[index] = [float(line[0]), -float(line[1])]
        index += 1
    return coordinates

def start_step4():
    map = Graph(14)

    # Label
    map.set_label_node(0, "Reactor")
    map.set_label_node(1, "UpperE")
    map.set_label_node(2, "LowerE")
    map.set_label_node(3, "Security")
    map.set_label_node(4, "Electrical")
    map.set_label_node(5, "Medbay")
    map.set_label_node(6, "Storage")
    map.set_label_node(7, "Cafetaria")
    map.set_label_node(8, "Unnamed1")
    map.set_label_node(9, "Unnamed2")
    map.set_label_node(10, "O2")
    map.set_label_node(11, "Weapons")
    map.set_label_node(12, "Shield")
    map.set_label_node(13, "Navigations")

    # Edge
    map.add_edge(("Reactor", "UpperE"), 9, by="label")
    map.add_edge(("Reactor", "Security"), 6, by="label")
    map.add_edge(("Reactor", "LowerE"), 9, by="label")
    map.add_edge(("UpperE", "LowerE"), 12, by="label")
    map.add_edge(("UpperE", "Security"), 9, by="label")
    map.add_edge(("UpperE", "Medbay"), 10, by="label")
    map.add_edge(("UpperE", "Cafetaria"), 15, by="label")
    map.add_edge(("Security", "LowerE"), 9, by="label")
    map.add_edge(("LowerE", "Electrical"), 14, by="label")
    map.add_edge(("LowerE", "Storage"), 14, by="label")
    map.add_edge(("Electrical", "Storage"), 10, by="label")
    map.add_edge(("Medbay", "Cafetaria"), 10, by="label")
    map.add_edge(("Cafetaria", "Storage"), 12, by="label")
    map.add_edge(("Cafetaria", "Unnamed1"), 11, by="label")
    map.add_edge(("Cafetaria", "Weapons"), 9, by="label")
    map.add_edge(("Storage", "Unnamed1"), 8, by="label")
    map.add_edge(("Storage", "Unnamed2"), 9, by="label")
    map.add_edge(("Weapons", "O2"), 7, by="label")
    map.add_edge(("Weapons", "Navigations"), 10, by="label")
    map.add_edge(("O2", "Navigations"), 10, by="label")
    map.add_edge(("O2", "Shield"), 13, by="label")
    map.add_edge(("Unnamed2", "Shield"), 6, by="label")
    map.add_edge(("Shield", "Navigations"), 12, by="label")
    map.add_edge(("Navigations", "Shield"), 12, by="label")

    map.kruskal(inplace=True)
    map.plot(position = read_coordinates("ADSA_Problem/Step4/coordinates.txt"))
    plt.show()
