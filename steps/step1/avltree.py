from collections import deque
import copy
from graphviz import Digraph
import random
from .player import Player

class NodePlayer:
    """Represent a node in the AVLTree class.

    :param value: The value of the node.
    :param NodePlayer left: The left child. (Default: None)
    :param NodePlayer right: The right child. (Default: None)
    :param int height: The height of the node. (Default: 0)
    """

    def __init__(self, player, left=None, right=None, height=0):
        self.player = player
        self.left = left
        self.right = right
        self.height = height

    def update_height(self):
        """Update the height of a node.

        Assigne to self.height the maximum height of its children plus one.
        """

        if self.left is None and self.right is None:
            self.height = 0
        elif self.left is None:
            self.height = self.right.height + 1
        elif self.right is None:
            self.height = self.left.height + 1
        else:
            self.height = max(self.left.height, self.right.height) + 1

    def get_balance_factor(self):
        """Compute the balance factor of a node

        Compute the difference between the heights of the right and left subtree.

        :return: The balance factor.
        :rtype: int
        """

        if self.left is None and self.right is None:
            return 0
        elif self.left is None:
            return self.right.height - (-1)
        elif self.right is None:
            return -1 - self.left.height
        else:
            return self.right.height - self.left.height

    def get_largest_child(self):
        """Return the largest child

        :return: The largest child.
        :rtype: TreeNode
        """

        if self.left is None and self.right is None:
            return None
        elif self.left is None:
            return self.right
        elif self.right is None:
            return self.left
        else:
            return self.left if self.left.value > self.right.value else self.right

    def __lt__(self, other):
        """Operator overloading of the lesser than operator.

        :param other: The node which is compared to `self`.
        :return: A boolean value indicating whether `self` is less than `other` or not.
        :rtype: bool
        """

        return self.player.score < other.player.score

    def __eq__(self, other):
        """Operator overloading of the equal operator.

        :param other: The node which is compared to `self`.
        :return: A boolean value indicating whether `self` equal than `other` or not.
        :rtype: bool
        """

        return self.player.value == other.player.value

    def __getattr__(self, key):
        if key == "value":
            return self.player.score
        elif key == "id":
            return self.player.id

    def __str__(self):
        return self.player.__str__()


class AVLTree:
    """An AVL tree implementation.

    :param NodePlayer root_node: The root node of the tree.
    :param int nb_node: The total number of nodes in the tree.
    """

    def __init__(self, nb_node=0):
        self.nb_node = 0
        self.root_node = None
        self.insert_nodes(NodePlayer(Player(i,0)) for i in range(nb_node))

    def _left_rotation(self, node):
        """Apply a left rotation to a node.

        :param NodePlayer node: NodePlayer where we apply the left rotation.
        :raise: AttributeError if node doesn't have a right child.
        """

        node_child = node.right
        node_child_subtree = node_child.left

        node_child.left = node
        node.right = node_child_subtree

        node.update_height()
        node_child.update_height()

        return node_child

    def _right_rotation(self, node):
        """Apply a left rotation to a node.

        :param NodePlayer node: NodePlayer where we apply the right rotation.
        :raise: AttributeError if node doesn't have a left child.
        """

        node_child = node.left
        node_child_subtree = node_child.right

        node_child.right = node
        node.left = node_child_subtree

        node.update_height()
        node_child.update_height()

        return node_child

    def _insert_node(self, current_node, node):
        """Insert a node in the tree and balance it afterward.

        :param NodePlayer current_node: Parent node.
        :param node: Key that is being inserted.
        :raise: TypeError if we try to insert a different type than self.root_node type or if the type of the tree doesn't support '<' operator.
        :return: A modified current_node with `node` inserted.
        :rtype: NodePlayer
        """

        # Insertion
        if current_node is None:
            current_node = node
        elif node < current_node:
            current_node.left = self._insert_node(current_node.left, node)
        else:
            current_node.right = self._insert_node(current_node.right, node)
        current_node.update_height()

        ## Balance
        balance_factor = current_node.get_balance_factor()
        if balance_factor > 1:
            if node < current_node.right:
                current_node.right = self._right_rotation(current_node.right)
                return self._left_rotation(current_node)
            else:
                return self._left_rotation(current_node)
        elif balance_factor < -1:
            if node < current_node.left:
                return self._right_rotation(current_node)
            else:
                current_node.left = self._left_rotation(current_node.left)
                return self._right_rotation(current_node)
        return current_node

    def insert_node(self, node):
        """Update some internal variables and call the insert method on node.

        :param node: Value of the node that is being inserted.
        :raise: TypeError if we try to insert a different type than self.root_node type or if the type of the tree doesn't support '<' operator.
        """

        self.nb_node += 1
        if self.root_node is None:
            self.root_node = node
        else:
            self.root_node = self._insert_node(self.root_node, node)

    def insert_nodes(self, nodes):
        """Insert multiple nodes in the tree.

        :param nodes: A list of node to insert in the tree.
        """

        for node in nodes:
            self.insert_node(node)

    def insert_keys(self, keys):
        """Construct NodePlayer instances with values in keys as score and insert them into the tree.

        :param iterable keys: A list of integer representing the score of new nodes inserted.
        """

        for key in keys:
            self.insert_node(NodePlayer(Player(0, key)))

    def _delete_key(self, current_node, key):
        """Delete a node from an AVL Tree

        :param NodePlayer current_node: Parent node.
        :param key: Value that is being deleted.
        :return: A modified current_node with `key` deleted or None.
        :rtype: NodePlayer or Nonde
        """

        if current_node is None:
            return current_node
        elif key < current_node.value:
            current_node.left = self._delete_key(current_node.left, key)
        elif key > current_node.value:
            current_node.right = self._delete_key(current_node.right, key)
        else:
            if current_node.left is None:
                return current_node.right
            elif current_node.right is None:
                return current_node.left
            else:
                working_node = current_node.right
                while working_node.left is not None:
                    working_node = working_node.left
                current_node.value = working_node.value
                current_node.right = self._delete_key(current_node.right, working_node.value)
        current_node.update_height()
        balance_factor = current_node.get_balance_factor()

        if balance_factor > 1:
            if current_node.right.get_balance_factor() < 0:
                current_node.right = self._right_rotation(current_node.right)
                return self._left_rotation(current_node)
            else:
                return self._left_rotation(current_node)
        elif balance_factor < -1:
            if current_node.left.get_balance_factor() > 0:
                current_node.left = self._left_rotation(current_node.left)
                return self._right_rotation(current_node)
            else:
                return self._right_rotation(current_node)
        return current_node

    def delete_key(self, key):
        """Delete a key of an AVL Tree if exist.

        :param key: The key that is deleted.
        :raise: AttributeError if key not in the tree. (But sometimes not, I don't know and don't have the force to search why)
        .. todo::
        Check if key is in the tree
        """

        self.root_node = self._delete_key(self.root_node, key)
        self.nb_node -= 1

    def delete_last(self, n=10):
        """Delete the n smallest value of the tree

        :param int n: The number of node to delete.
        ..todo:
            Optimize this function, indeed we can avoid traverse all the left branch every time.
        """

        for i in range(n):
            node = self.root_node
            while node.left is not None:
                node = node.left
            self.delete_key(node.value)

    def _copy_nodes(self, node, new_AVLTree):
        """Insert the all the values of the tree into antother AVLTree.

        :param AVLTree new_AVLTree: The AVLTree where we insert the nodes.
        """

        if node is not None:
            self._copy_nodes(node.left, new_AVLTree)
            new_AVLTree.insert_node(NodePlayer(Player(node.player.id, node.player.score)))
            self._copy_nodes(node.right, new_AVLTree)

    def copy_nodes(self, new_AVLTree):
        """Copy all nodes of `self` into a new AVLTree.

        :param AVLTree new_AVLTree: The AVLTree where we insert the nodes.
        """

        self._copy_nodes(self.root_node, new_AVLTree)

    def add_values(self, values, traversal = "inorder"):
        """Set values of the tree in a defined order.

        Set the values of the tree. The length of `values` doesn't need to be equal to the number of nodes in the tree.

        :param iterable values: Values to set.
        :param str type: String representing the type of traversal to perform when setting the values.
        """

        if traversal == "inorder":
            self._add_values_inorder(values)
        elif traversal == "preorder":
            self._add_values_preorder(values)

    def _add_values_inorder(self, values):
        """Set the values of the tree to values in an in-order traversal.

        :param values: A list of new values of the tree nodes.
        """

        s = deque()
        node = self.root_node
        index = 0
        while s or node is not None:
            if node is not None:
                s.append(node)
                node = node.left
            else:
                node = s.pop()
                node.player.score += values[index] # Something wrong with this. Need to clean __getattr__ and __setattr__ in NodePlayer.
                index += 1
                if index >= len(values):
                    break
                node = node.right

    def display_cli(self, data=True, node=None, sep='|', height=False, parent=False, balance=False, index=False, adress=False, id=False):
        """Display the tree in the console.

        :param bool data: Display the height and the number of nodes of the tree if True. (Default: True)
        :param NodePlayer node: The node which subtree is displayed. (Default: None)
        :param str sep: String chosen to seprate nodes. (Default: '|')
        :param bool height: Display the height of each key if True. (Default: False)
        :param bool parent: Display the parent of each key if True. (Default: False)
        :param bool balance: Display the balance factor of each key if True. (Default: False)
        :param bool index: Display the index of each key following a Breadth First search ordering if True. (Default: False)
        :param bool adress: Display the address of each node if True. (Default: False)
        :param bool id: Display the id of each node if True. (Default: False)
        """

        if node is None:
            node = self.root_node
        if node is None:
            return None
        current_list = deque()
        current_list.append((node, None))
        index_nb = 0
        next_list = deque()
        while current_list:
            while current_list:
                current_node, parent_index = current_list.popleft()
                print(sep,current_node.value,sep, end = '')
                if height:
                    print('<h', current_node.height, '>', sep =  '', end = '')
                if parent:
                    print('<p', parent_index, '>', sep = '', end = '')
                if balance:
                    print('<b', current_node.get_balance_factor(), '>', sep = '', end = '')
                if index:
                    print('<i', index_nb, '>', sep = '', end = '')
                if adress:
                    print('<a', current_node, '>', sep = '', end = '')
                if id:
                    print('<id', current_node.id, '>', sep = '', end = '')
                if current_node.left is not None:
                    next_list.append((current_node.left, index_nb))
                if current_node.right is not None:
                    next_list.append((current_node.right, index_nb))
                index_nb += 1
            print()
            current_list = next_list.copy()
            next_list.clear()
        if data:
            print("Height:", self.root_node.height)
            print("Number of nodes:", self.nb_node)

    def plot_graphviz(self, data=True, node=None, sep='|', height=False, parent=False, balance=False, index=False, adress=False, id=False):
        """Construct a graphviz Digraph of the tree.

        :param bool data: Display the height and the number of nodes of the tree if True. (Default: True)
        :param NodePlayer node: The node whose subtree is displayed. (Default: None)
        :param str sep: String chosen to seprate nodes. (Default: '|')
        :param bool height: Display the height of each node if True. (Default: False)
        :param bool parent: Display the parent of each node if True. (Default: False)
        :param bool balance: Display the balance factor of each node if True. (Default: False)
        :param bool index: Display the index of each node following a Breadth First search ordering if True. (Default: False)
        :param bool adress: Display the address of each node if True. (Default: False)
        :param bool id: Display the id of each node if True. (Default: False)
        """

        dot = Digraph()
        if node is None:
            node = self.root_node
        current_list = deque()
        current_list.append((node, None))
        index_nb = 0
        next_list = deque()
        while current_list:
            while current_list:
                current_node, parent_index = current_list.popleft()
                label = str(current_node.value)+'\n'
                if height:
                    label += '<h {}>\n'.format(current_node.height)
                if parent:
                    label += '<p {}>\n'.format(parent_index)
                if balance:
                    label += '<b {}>\n'.format(current_node.get_balance_factor())
                if index:
                    label += '<i {}>\n'.format(index_nb)
                if adress:
                    label += '<a {}>\n'.format(adress)
                if id:
                    label += '<id {}>\n'.format(current_node.id)
                if current_node.left is not None:
                    next_list.append((current_node.left, index_nb))
                if current_node.right is not None:
                    next_list.append((current_node.right, index_nb))
                dot.node(str(index_nb), label)
                if parent_index is not None:
                    dot.edge(str(parent_index), str(index_nb))
                index_nb += 1
            current_list = next_list.copy()
            next_list.clear()
        return dot

    def __getattr__(self, key):
        if key == "nb_player":
            return self.nb_node

    def _compute_nb_node(self):
        """Method to compute the number of nodes inside the tree."""

        s = deque()
        nb = 0
        node = self.root_node
        while s or node is not None:
            if node is not None:
                s.append(node)
                node = node.left
            else:
                node = s.pop()
                nb += 1
                node = node.right
        return nb

    def __str__(self):
        descrition = ""
        s = deque()
        node = self.root_node
        while s or node is not None:
            if node is not None:
                s.append(node)
                node = node.left
            else:
                node = s.pop()
                descrition += node.__str__() + '\n'
                node = node.right
        return descrition[:-1]

    def __len__(self):
        return self.nb_node
