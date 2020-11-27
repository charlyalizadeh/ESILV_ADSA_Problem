#!/usr/bin/env python3
import numpy as np
from math import inf
from copy import copy
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
from .UnionFind import UnionFind

class Graph():
    def __init__(self, nb_nodes=0):
        self.adj_matrix = np.ones((nb_nodes, nb_nodes)) * inf
        self.label = [i for i in range(nb_nodes)]

    def get_edges(self, weight=True):
        """Get the edges from the graph.

        :param bool weight: Add the weight in the return tuples if True. (Default True)
        :return: A list of tuple, each tuple representing one edge.
        :rtype: list
        """

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
        """Get the neighbors of a node.

        :param int node: The node whose neighbors are computed.
        :return: A list of integer representing the neighbors of `node`.
        :rtype: list
        """

        neighbors = []
        for i in range(self.adj_matrix.shape[0]):
            if self.adj_matrix[i, j] != inf:
               neighbors.append(i)
        return neighbors

    def rem_edge(self, edge):
        """Delete an edge from the graph

        :param iterable edge: A iterable representing an edge.
        """

        i, j = edge
        self.adj_matrix[i, j] = inf
        self.adj_matrix[j, i] = inf

    def rem_edges(self, edges):
        """Delete multiple edge from the graph.

        :param iterable edges: An iterable containing the edges to be deleted.
        """

        for edge in edges:
            self.rem_edge(edge)

    def rem_all_edges(self):
        """Delete all the edges from the graph."""

        dimension = self.adj_matrix.shape[0]
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

    def set_label_node(self, node, label):
        """Set the label of a node.

        :param int node: The index of the node whose label.
        :param str label: The label of the index.
        """

        if node >= len(self.label):
            raise ValueError("`node` doesn't exist in the current graph.")
        self.label[node] = label

    def plot(self, label_as_index=False, position=None):
        """Plot the graph in a matplotlib graph.

        :param bool label_as_index: Display the index node instead of the label if True. (Default False)
        :param iterable position: The position for the
        """

        G = nx.Graph()
        G.add_nodes_from([(i , {"label":self.label[i]}) for i in range(len(self.label))])
        edges = self.get_edges()
        for edge in edges:
            G.add_edge(edge[0], edge[1], weight = edge[2])
        pos = nx.planar_layout(G) if position is None  else position
        nx.draw(G, pos, with_labels = False, font_weight = 'bold')
        nx.draw_networkx_labels(G, pos, dict(zip(range(len(self.label)),self.label)))
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels = labels)

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
