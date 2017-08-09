from empty import Empty
from node import Node

import sys


class BinaryTree(object):
    def __init__(self):
        self.top = Empty()

    def shift_left(self, node):
        # pre = len(node)
        new_top_value = node.right.minimum()
        node.right = self._do_delete(node.right, new_top_value)
        new_top = Node(new_top_value)
        new_top.left = node.left
        new_top.right = node.right
        # assert (len(new_top) == pre -1)
        return self._do_insert(new_top, node.value)

    def shift_right(self, node):
        # pre = len(node)
        new_top_value = node.left.maximum()
        # pre2 = len(node.left)
        # node.left.show(1000)
        node.left = self._do_delete(node.left, new_top_value)
        # node.left.show(1000)
        # print "-----", pre2, len(node.left), new_top_value
        # assert (len(node.left) == pre2 -1)
        new_top = Node(new_top_value)
        new_top.left = node.left
        new_top.right = node.right
        # assert (len(new_top) == pre -1)
        return self._do_insert(new_top, node.value)

    def check2(self, node):
        diff = node.left.max_length - node.right.max_length
        if diff < -1:
            return self.shift_left(node)
        if diff > 1:
            return self.shift_right(node)
        node.max_length = max(node.left.max_length, node.right.max_length) + 1
        return node

    def rotate_left(self, node):
        new_top = node.right
        node.right = new_top.left
        new_top.left = node
        node.max_length = max(node.left.max_length, node.right.max_length) + 1
        return self.check2(new_top)

    def rotate_right(self, node):
        new_top = node.left
        node.left = new_top.right
        new_top.right = node
        node.max_length = max(node.left.max_length, node.right.max_length) + 1
        return self.check2(new_top)

    def check(self, node):
        diff = node.left.max_length - node.right.max_length
        if diff < -1:
            return self.rotate_left(node)
        if diff > 1:
            return self.rotate_right(node)
        node.max_length = max(node.left.max_length, node.right.max_length) + 1
        return node

    def _do_insert(self, node, new_value):
        if node.is_empty():
            return Node(new_value)
        if new_value < node.value:
            node.left = self._do_insert(node.left, new_value)
        else:
            node.right = self._do_insert(node.right, new_value)
        return self.check(node)

    def _do_delete(self, node, value):
        if value < node.value:
            node.left = self._do_delete(node.left, value)
            return self.check(node)
        if value == node.value:
            if node.left.is_empty():
                return node.right
            elif node.right.is_empty():
                return node.left
            else:
                node.value = node.right.minimum()
                node.right = self._do_delete(node.right, node.value)
                return self.check(node)
        node.right = self._do_delete(node.right, value)
        return self.check(node)

    def insert(self, value):
        self.top = self._do_insert(self.top, value)

    def delete(self, value):
        self.top = self._do_delete(self.top, value)

    def show(self, level=sys.maxint):
        self.top.show(level)

    def __len__(self):
        return len(self.top)

    def balanced(self):
        return self.top.balanced()

    def __iter__(self):
        for value in self.top:
            yield value
