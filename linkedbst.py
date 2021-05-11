'''
Module represents binary search tree
'''
import random
import time
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top: any
            :return: int
            '''
            if top is None:
                return -1
            else:
                return 1 + max(height1(top.left), height1(top.right))
        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return: bool
        '''
        formula = (2 * log(self._size + 1, 2)) - 1
        if self.height() < formula:
            return True
        else:
            return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low: int
        :param high: int
        :return: list
        '''
        lst = []
        result_lst = []
        for elem in self:
            lst.append(elem)
        for elem in sorted(lst):
            if elem >= low and elem <= high:
                result_lst.append(elem)
        return result_lst


    def rebalance(self):
        '''
        Rebalances the tree.
        :return: LinkedBST()
        '''
        lst = []
        for elem in self:
            lst.append(elem)
        lstt = sorted(lst)
        bstt = LinkedBST()
        def rebalance1(bst, lst):
            if not lst:
                return None
            mid = (len(lst)) // 2
            bst.add(lst[mid])
            rebalance1(bst, lst[:mid])
            rebalance1(bst, lst[mid+1:])
            return bst
        self.clear()
        return rebalance1(bstt, lstt)


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item: int
        :type item: any
        :return: int
        """
        lst = []
        for elem in self:
            if elem > item:
                lst.append(elem)
        if len(lst) == 0:
            return None
        else:
            return min(lst)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item: int
        :type item: any
        :return: int
        """
        lst = []
        for elem in self:
            if elem < item:
                lst.append(elem)
        if len(lst) == 0:
            return None
        else:
            return max(lst)


    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path: path to file
        :type path: str
        :return: string with time of search
        :rtype: str
        """
        lst = []
        with open(path, 'r') as file:
            for i in file:
                lst.append(i[:-1])
        
        start_time1 = time.time()
        small_lst = []
        for _ in range(10000):
            small_lst.append(random.choice(lst))
        
        for i in small_lst:
            i in lst
        time1 = time.time() - start_time1

        start_time2 = time.time()
        bst = LinkedBST()
        for word in lst[:900]:
            bst.add(word)

        for _ in range(10000):
            bst.find(random.choice(lst[:900]))
        time2 = time.time() - start_time2

        start_time3 = time.time()
        tree = LinkedBST()
        for _ in range(len(lst)):
            tree.add(random.choice(lst))
        
        for _ in range(10000):
            tree.find(random.choice(lst))
        time3 = time.time() - start_time3

        start_time4 = time.time()
        balansed_tree = tree.rebalance()

        for _ in range(10000):
            balansed_tree.find(random.choice(lst))
        time4 = time.time() - start_time4

        return f"Find 10000 words from list - {time1} sec.\n\
Find 10000 words from binary tree (sorted in alphabetic order) - {time2} sec.\n\
Find 10000 words from binary tree (random order) - {time3} sec.\n\
Find 10000 words from balanced binary tree - {time4} sec."