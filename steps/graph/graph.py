from math import inf
import numpy as np
from copy import copy
import networkx as nx
from .unionfind import UnionFind
from utils.utils import read_coordinates


class Graph():
    """
    Graph implementation with an adjacency matrix.

    :param int nb_vertex: Number of vertices to initialize the graph with. (Default 0)
    """

    def __init__(self, nb_vertex=0):
        self.adj_matrix = np.ones((nb_vertex, nb_vertex)) * inf
        self.label = [i for i in range(nb_vertex)]
        for i in range(nb_vertex):
            self.adj_matrix[i, i] = 0

    def get_edges(self, weight=True):
        """Get the edges from the graph.

        :param bool weight: Add the weight in the return tuples if True. (Default True)
        :return: A list of tuple, each tuple representing one edge.
        :rtype: list
        """

        edges = []
        for i in range(self.nb_vertex - 1):
            for j in range(i + 1, self.nb_vertex):
                if self.adj_matrix[i, j] != inf:
                    if weight:
                        edges.append((i, j, self.adj_matrix[i, j]))
                    else:
                        edges.append((i, j))
        return edges

    def get_neighbors(self, vertex):
        """Get the neighbors of a vertex.

        :param int vertex: The vertex whose neighbors are computed.
        :return: A list of integer representing the neighbors of `vertex`.
        :rtype: list
        """

        neighbors = []
        for i in range(self.nb_vertex):
            if self.are_neighbors(vertex, i) and vertex != i:
                neighbors.append(i)
        return neighbors

    def are_neighbors(self, vertex1, vertex2):
        """Check if `vertex1` and `vertex2` are neighbors.

        :param int vertex1: the index of the first vertex.
        :param int vertex2: the index of the second vertex.
        :return: `True` if `vertex1` and `vertex2` are neighbors, `False` otherwise.
        :rtype: bool
        """

        return (self.adj_matrix[vertex1, vertex2], self.adj_matrix[vertex2, vertex1]) != (inf, inf)

    def rem_edge(self, edge):
        """Delete an edge from the graph

        :param iterable edge: A iterable representing an edge.
        """

        i, j = edge
        self.adj_matrix[i, j] = inf
        self.adj_matrix[j, i] = inf

    def rem_edges(self, edges):
        """Delete multiple edges from the graph.

        :param iterable edges: An iterable containing the edges to be deleted.
        """

        for edge in edges:
            self.rem_edge(edge)

    def rem_all_edges(self):
        """Delete all the edges from the graph."""

        dimension = self.nb_vertex
        self.adj_matrix = np.ones((dimension, dimension)) * inf

    def add_edge(self, edge, weight=1, by="index"):
        """Add an edge to the graph.

        :param iterable edge: An iterable representing the edge to be added.
        :param weight: The weight of the edge. (Default 1)
        :param str by: The method used to add edge. (Default "index")
        """

        if by == "index":
            self.adj_matrix[edge[0], edge[1]] = weight
            self.adj_matrix[edge[1], edge[0]] = weight
        elif by == "label":
            index1 = self.label.index(edge[0])
            index2 = self.label.index(edge[1])
            self.adj_matrix[index1, index2] = weight
            self.adj_matrix[index2, index1] = weight

    def add_edges(self, edges, weights=None):
        """Add multiple edges to the graph.

        :param iterable edges: An iterable containing the edges to be added.
        :param iterable weights: An iterable containing the weights of the new edges. (Default None)
        """

        if weights is None:
            weights = [1] * len(edges)
        elif len(weights) != len(edges):
            raise ValueError("weights must be the same length as edges.")
        for i in range(len(edges)):
            self.add_edge(edges[i], weights[i])

    def add_vertex(self, label=""):
        """Add a vertex to the graph.

        :param str label: label for the vertex whose being added to the graph. (Default "")
        """

        if self.nb_vertex == 0:
            self.adj_matrix = np.array([0])
        elif self.nb_vertex == 1:
            self.adj_matrix = np.array([[0, inf], [inf, 0]])
        else:
            self.adj_matrix = np.vstack((self.adj_matrix, np.ones(self.adj_matrix.shape[1]) * inf))
            self.adj_matrix = np.column_stack((self.adj_matrix, np.ones(self.nb_vertex) * inf))
            shape0, shape1 = self.adj_matrix.shape
            self.adj_matrix[shape0 - 1, shape1 - 1] = 0

    def set_label_vertex(self, vertex, label):
        """Set the label of a vertex.

        :param int vertex: The index of the vertex whose label.
        :param str label: The label of the index.
        """

        if vertex >= len(self.label):
            raise ValueError("`vertex` doesn't exist in the current graph.")
        self.label[vertex] = label

    def _import_from_file_specific_index(self, lines):
        index = 1
        if "INDEX" in lines[0]:
            while not (lines[index].rstrip("\n").isspace() or lines[index] == "\n"):
                self.add_vertex()
                self.label.append(lines[index].rstrip("\n"))
                index += 1
        index += 1
        for line in lines[index:]:
            line = line.split(",")
            self.add_edge(line[:2], weight=int(line[2].strip("\n")), by="label")

    def _import_from_file(self, lines):
        for line in lines:
            line = line.split(",")
            for label in line[:2]:
                if label not in self.label:
                    self.add_vertex()
                    self.label.append(label)
            self.add_edge(line[:2], weight=int(line[2].strip("\n")), by="label")

    def import_from_file(self, filename):
        """Import a graph from a file. (!! Doesn't support same label for two different vertices. !!)

        :param str filename: the name of the file containing the graph data.
        """

        self.adj_matrix = np.array([])
        self.label.clear()
        with open(filename, "r") as file:
            lines = file.readlines()
            if lines[0].rstrip("\n") == "INDEX":
                self._import_from_file_specific_index(lines)
            else:
                self._import_from_file(lines)

    def plot(self, label_as_index=False, position=None, filepos=None):
        """Plot the graph in a matplotlib graph.

        :param bool label_as_index: Display the index vertex instead of the label if True. (Default False)
        :param iterable position: The position for the
        """

        G = nx.Graph()
        G.add_nodes_from([(i, {"label": self.label[i]}) for i in range(len(self.label))])
        edges = self.get_edges()
        for edge in edges:
            G.add_edge(edge[0], edge[1], weight=edge[2])
        if filepos is not None:
            pos = read_coordinates(filepos)
        elif position is not None:
            pos = position
        else:
            pos = nx.planar_layout(G) if position is None else position
        nx.draw(G, pos, with_labels=label_as_index, font_weight='bold')
        if not label_as_index:
            nx.draw_networkx_labels(G,
                                    pos,
                                    dict(zip(range(len(self.label)), self.label)))
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    def kruskal(self, inplace=False):
        """Apply Kruskal algorithm to the graph.

        :param bool inplace: Remove the edge not in the spanning tree if True. (Default False)
        :return: The edges of the spanning tree and the total weight of the tree.
        :rtype: tuple
        """

        spanning_tree_edges, weight = self._kruskal()
        if inplace:
            self.rem_all_edges()
            for edge in spanning_tree_edges:
                self.add_edge(edge[:2], edge[2])
        return spanning_tree_edges, weight

    def _kruskal(self):
        """Apply Kruskal algorithm to the graph.

        :return: The edges of the spanning tree and the total weight of the tree.
        :rtype: tuple
        """

        disjoint_set = UnionFind()
        s = set()
        for i in range(self.nb_vertex):
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

    def floydWarshall(self):
        """Return the minimal distances between every vertex.
        :param matrix: Matrix of adjacency of a graph.
        :return: Matrix of minimal distances between every vertex.
        """

        self.dist = copy(self.adj_matrix)
        for k in range(len(self.adj_matrix)):
            for i in range(len(self.adj_matrix)):
                for j in range(len(self.adj_matrix)):
                    self.dist[i][j] = min(self.dist[i][j], self.dist[i][k] + self.dist[k][j])
        return self.dist

    def get_shortest_path(self, paths):
        """Get the shortest path between multiple path.

        :param iterable paths: An iterable containing the paths.
        :return: The shortest path in `paths`.
        :rtype: iterable
        """

        best_path = paths[0]
        best_weight = self.get_path_weight(paths[0])
        for path in paths[1:]:
            weight = self.get_path_weight(path)
            if weight < best_weight:
                best_weight = weight
                best_path = path
        return best_path, best_weight

    def get_path_weight(self, path):
        """Compute the weight of `path`.

        :param iterable path: The path whose weight is computed.
        :return: The weight of `path`.
        :rtype: int
        """

        weight = 0
        for i in range(len(path) - 1):
            weight += self.adj_matrix[path[i], path[i + 1]]
        return weight

    def get_shortest_path_all_hamilton_path(self):
        """Compute all the shortest Hamtilon paths in the graph.

        :param iterable starting_vertex: An iterable containing the starting vertices.
        :param iterable ending_vertex: An iterable containing the ending vertices.
        :return: The shortest path if such a path exists, None otherwise.
        :rtype: list or None
        """

        return self.get_shortest_hamilton_path(range(self.nb_vertex), range(self.nb_vertex))

    def get_shortest_hamilton_path(self, starting_vertex=None, ending_vertex=None):
        """Compute the shortest hamilton path such a path exists."""

        all_path = self.get_hamilton_path(starting_vertex, ending_vertex)
        if not all_path:
            return None
        return self.get_shortest_path(all_path)

    def get_all_hamilton_path(self):
        """Compute all the possible hamilton paths.

        :return: A list containing all the Hamilton paths in the graph.
        :rtype: list
        """

        return self.get_hamilton_path(range(self.nb_vertex), range(self.nb_vertex))

    def get_hamilton_path(self, starting_vertex=None, ending_vertex=None):
        """Compute all the hamilton starting in `starting_vertex` and ending in `ending_vertex`.

        :param iterable starting_vertex: An iterable containing the starting vertices.
        :param iterable ending_vertex: An iterable containing the ending vertices.
        :return: An list containing all the valid Hamilton paths.
        :rtype: list
        """

        all_path = []
        for i in starting_vertex:
            self._backtrack_hamilton([i], all_path)
        all_path = [path for path in all_path if path[-1] in ending_vertex]
        return all_path

    def _backtrack_hamilton(self, path, all_path):
        """Recursive algorithm to compute all the hamilton path starting at path[0].

        :param iterable path: The current path being tested.
        :param iterable all_path: An iterable storing all the hamilton path.
        """

        if path.count(path[-1]) == 2:
            return None
        elif len(path) == self.nb_vertex:
            all_path.append(path)
        for n in self.get_neighbors(path[-1]):
            new_path = path + [n]
            self._backtrack_hamilton(new_path, all_path)

    def set_path(self, vertices):
        """Convert the graph to a path graph

        :param iterable vertices: Path to be converted to.
        """

        edges = [(vertices[i], vertices[i + 1]) for i in range(len(vertices) - 1)]
        weights = [self.adj_matrix[edge[0], edge[1]] for edge in edges]
        self.rem_all_edges()
        for i in range(len(edges)):
            self.add_edge(edges[i], weights[i])

    def __getattr__(self, key):
        if key == "nb_vertex":
            return self.adj_matrix.shape[0]
        if key == "nb_edge":
            return len(self.get_edges())  # TODO: more efficient solution.

    def __str__(self):
        return self.adj_matrix.__str__()
