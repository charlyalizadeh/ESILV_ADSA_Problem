import pandas as pd

class UnionFind:
    """Disjoint-set data structure implementation """

    def __init__(self):
        self.parents = []
        self.index_map = {}
        self.size = []

    def make_set(self, node):
        if node not in self.index_map.keys():
            index = len(self.parents)
            self.parents.append(index)
            self.index_map[node] = index
            self.size.append(1)

    def make_sets(self, nodes):
        for node in nodes:
            self.make_set(node)

    def find(self, node):
        if self.index_map[node] != self.parents[self.index_map[node]]:
            self.parents[self.index_map[node]] = self.find(self.parents[self.index_map[node]])
            return self.parents[self.index_map[node]]
        else:
            return self.index_map[node]

    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)
        if root1 == root2:
            return None
        if self.size[root1] < self.size[root2]:
            root1, root2 = root2, root1
        self.parents[root2] = root1
        self.size[root1] += self.size[root2]

    def __str__(self):
        nodes = self.index_map.keys()
        index = [self.index_map[n] for n in nodes]
        sizes = [self.size[i] for i in index]
        parents = [self.parents[i] for i in index]
        df = pd.DataFrame({"element": nodes,
                           "index": index,
                           "size": sizes,
                           "parent": parents
                           })
        return df.__str__()
