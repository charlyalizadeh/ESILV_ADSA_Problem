from collections import deque
import copy
from graphviz import Digraph

class TreeNode:
    """Represent a node in the AVLTree class.

    :param value: The value of the node.
    :param TreeNode left: The left child. (Default: None)
    :param TreeNode right: The right child. (Default: None)
    :param int height: The height of the node. (Default: 0)
    """

    def __init__(self, value, left=None, right=None, height=0):
        self.value = value
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

class AVLTree:
    """An AVL tree implementation.

    :param TreeNode root_node: The root node of the tree. (Default: None)
    :param int nb_node: The total number of nodes in the tree.
    """

    def __init__(self, root_node=None):
        self.root_node = root_node
        self.nb_node = 0 if root_node is None else 1

    def _left_rotation(self, node):
        """Apply a left rotation to a node.

        :param TreeNode node: Node where we apply the left rotation.
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

        :param TreeNode node: Node where we apply the right rotation.
        :raise: AttributeError if node doesn't have a left child.
        """

        node_child = node.left
        node_child_subtree = node_child.right

        node_child.right = node
        node.left = node_child_subtree

        node.update_height()
        node_child.update_height()

        return node_child

    def _insert_node(self, current_node, key):
        """Insert a node in the tree and balance it afterward.

        :param TreeNode current_node: Parent node.
        :param key: Key whose being inserted.
        :raise: TypeError if we try to insert a different type than self.root_node type or if the type of the tree doesn't support '<' operator.
        :return: A modified current_node with `key` inserted.
        :rtype: TreeNode
        """

        # Insertion
        if current_node is None:
            current_node = TreeNode(key)
        elif key < current_node.value:
            current_node.left = self._insert_node(current_node.left, key)
        else:
            current_node.right = self._insert_node(current_node.right, key)
        current_node.update_height()

        ## Balance
        balance_factor = current_node.get_balance_factor()
        if balance_factor > 1:
            if key < current_node.right.value:
                current_node.right = self._right_rotation(current_node.right)
                return self._left_rotation(current_node)
            else:
                return self._left_rotation(current_node)
        elif balance_factor < -1:
            if key < current_node.left.value:
                return self._right_rotation(current_node)
            else:
                current_node.left = self._left_rotation(current_node.left)
                return self._right_rotation(current_node)
        return current_node

    def insert_node(self, key):
        """Update some internal variables and call the insert method on key.

        :param key: Value of the node whose being inserted.
        :raise: TypeError if we try to insert a different type than self.root_node type or if the type of the tree doesn't support '<' operator.
        """

        self.nb_node += 1
        if self.root_node is None:
            self.root_node = TreeNode(key)
        else:
            self.root_node = self._insert_node(self.root_node, key)

    def insert_nodes(self, keys):
        """Insert multiple nodes in the tree.

        :param keys: A list of key to insert in the tree.
        """

        for key in keys:
            self.insert_node(key)

    def _delete_node(self, current_node, key):
        """Delete a node from an AVL Tree

        :param TreeNode current_node: Parent node.
        :param key: Value whose being deleted.
        :return: A modified current_node with `key` deleted or None.
        :rtype: TreeNode or Nonde
        """

        if current_node is None:
            return current_node
        elif key < current_node.value:
            current_node.left = self._delete_node(current_node.left, key)
        elif key > current_node.value:
            current_node.right = self._delete_node(current_node.right, key)
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
                current_node.right = self._delete_node(current_node.right, working_node.value)
        current_node.update_height()
        balance_factor = current_node.get_balance_factor()

        child = current_node.get_largest_child()
        grand_child = child.get_largest_child()
        if balance_factor > 1:
            if grand_child.value < child.value:
                current_node.right = self._right_rotation(current_node.right)
                return self._left_rotation(current_node)
            else:
                return self._left_rotation(current_node)
        elif balance_factor < -1:
            if grand_child.value < child.value:
                return self._right_rotation(current_node)
            else:
                current_node.left = self._left_rotation(current_node.left)
                return self._right_rotation(current_node)
        return current_node

    def delete_node(self, key):
        """Delete a key of an AVL Tree if exist.

        :param key: The key whose being deleted.
        :raise: AttributeError if key not in the tree. (But sometimes not, I don't know and don't have the force to search why)
        .. todo::
        Check if key is in the tree
        """

        new_root = self._delete_node(self.root_node, key)
        if new_root is not None:
            self.root_node = new_root
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
            self.delete_node(node.value)

    def display_cli(self, data=True, node=None, sep='|', height=False, parent=False, balance=False, index=False):
        """Display the tree in the console.

        :param bool data: Display the height and the number of nodes of the tree if True. (Default: True)
        :param TreeNode node: The node whose subtree is displayed. (Default: None)
        :param str sep: String chosen to seprate nodes. (Default: '|')
        :param bool height: Display the height of each key if True. (Default: False)
        :param bool parent: Display the parent of each key if True. (Default: False)
        :param bool balance: Display the balance factor of each key if True. (Default: False)
        :param bool index: Display the index of each key following a Breadth First search ordering if True. (Default: False)
        """

        if node is None:
            node = self.root_node
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

    def plot_graphviz(self, data=True, node=None, sep='|', height=False, parent=False, balance=False, index=False):
        """Construct a graphviz Digraph of the tree.

        :param bool data: Display the height and the number of nodes of the tree if True. (Default: True)
        :param TreeNode node: The node whose subtree is displayed. (Default: None)
        :param str sep: String chosen to seprate nodes. (Default: '|')
        :param bool height: Display the height of each key if True. (Default: False)
        :param bool parent: Display the parent of each key if True. (Default: False)
        :param bool balance: Display the balance factor of each key if True. (Default: False)
        :param bool index: Display the index of each key following a Breadth First search ordering if True. (Default: False)
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
