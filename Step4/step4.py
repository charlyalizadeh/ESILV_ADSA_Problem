import numpy as np
from math import inf
from copy import copy
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
from UnionFind import UnionFind

class Graph():
    def __init__(self, nb_vertices=0):
        self.adj_matrix = np.ones((nb_vertices, nb_vertices)) * inf
        self.label = [i for i in range(nb_vertices)]

    def get_edges(self, weight=True):
        edges = []
        for i in range(self.adj_matrix.shape[0] - 1):
            for j in range(i + 1, self.adj_matrix.shape[0]):
                if self.adj_matrix[i, j] != inf:
                    if weight:
                        edges.append((i, j, self.adj_matrix[i, j]))
                    else:
                        edges.append((i, j))
        return edges

    def get_neighbors(self, node):
        neighbors = []
        for i in range(self.adj_matrix.shape[0]):
            if self.adj_matrix[i, j] != inf:
               neighbors.append(i)
        return neighbors

    def rem_edge(self, edge):
        i, j = min(edge), max(edge)
        self.adj_matrix[i, j] = inf

    def rem_edges(self, edges):
        for edge in edges:
            self.rem_edge(edge)

    def rem_all_edges(self):
        dimension = self.adj_matrix.shape[0]
        self.adj_matrix = np.ones((dimension, dimension)) * inf

    def add_edge(self, edge, weight=1, by="index"):
        if by == "index":
            self.adj_matrix[edge[0], edge[1]] = weight
            self.adj_matrix[edge[1], edge[0]] = weight
        elif by == "label":
            index1 = self.label.index(edge[0])
            index2 = self.label.index(edge[1])
            self.adj_matrix[index1, index2] = weight
            self.adj_matrix[index2, index1] = weight

    def add_edges(self, edges, weights=None):
        if weights is None:
            weights = [1] * len(edges)
        elif len(weights) != len(edges):
            raise ValueError("weights must be the same length as edges.")
        for i in range(len(edges)):
            self.add_edge(edges[i], weights[i])

    def set_label_vertex(self, vertex, label):
        self.label[vertex] = label
    def plot(self, label_as_index=False, position=None):
        G = nx.Graph()
        G.add_nodes_from([(i , {"label":self.label[i]}) for i in range(len(self.label))])
        edges = self.get_edges()
        for edge in edges:
            G.add_edge(edge[0], edge[1], weight = edge[2])
        pos = nx.planar_layout(G) if position is None  else position
        print(pos)
        nx.draw(G, pos, with_labels = False, font_weight = 'bold')
        nx.draw_networkx_labels(G, pos, dict(zip(range(len(self.label)),self.label)))
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels = labels)

    def kruskal(self, inplace=False):
        spanning_tree_edges, weight = self._kruskal()
        if inplace:
            self.rem_all_edges()
            for edge in spanning_tree_edges:
                self.add_edge(edge[:2], edge[2])
        return spanning_tree_edges, weight

    def _kruskal(self):
        disjoint_set = UnionFind()
        s = set()
        for i in range(self.adj_matrix.shape[0]):
            disjoint_set.make_set(i)
        edges = self.get_edges()
        edges = sorted(edges, key=lambda e: e[2])
        for edge in edges:
            root1 = disjoint_set.find(edge[0])
            root2 = disjoint_set.find(edge[1])
            if  root1 != root2:
                s.add(edge)
                disjoint_set.union(root1, root2)
        return s, sum([e[2] for e in s])

    def __str__(self):
        return self.adj_matrix.__str__()



map = Graph(14)
# Label
map.set_label_vertex(0, "Reactor")
map.set_label_vertex(1, "UpperE")
map.set_label_vertex(2, "LowerE")
map.set_label_vertex(3, "Security")
map.set_label_vertex(4, "Electrical")
map.set_label_vertex(5, "Medbay")
map.set_label_vertex(6, "Storage")
map.set_label_vertex(7, "Cafetaria")
map.set_label_vertex(8, "Unnamed1")
map.set_label_vertex(9, "Unnamed2")
map.set_label_vertex(10, "O2")
map.set_label_vertex(11, "Weapons")
map.set_label_vertex(12, "Shield")
map.set_label_vertex(13, "Navigations")

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


def read_coordinates(filename):
    file = open(filename, "r")
    coordinates = {}
    index = 0
    for line in file.readlines():
        line = line.split(",")
        coordinates[index] = [float(line[0]), -float(line[1])]
        index += 1
    return coordinates


map.kruskal(inplace=True)
map.plot(position = read_coordinates("coordinates.txt"))
plt.show()
