class Node(object):

    __slots__ = ("left", "right", "value")

    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value


def show(node, tab=""):
    if node is None:
        return
    show(node.left, tab+"    ")
    print tab, node.value
    show(node.right, tab+"    ")


def insert(node, new_value):
    if node is None:
        return Node(new_value)
    if new_value < node.value:
        node.left = insert(node.left, new_value)
    else:
        node.right = insert(node.right, new_value)
    return node


def has_value(node, value):
    if node is None:
        return False
    if value < node.value:
        return has_value(node.left, value)
    elif value == node.value:
        return True
    else:
        return has_value(node.right, value)


def minimum(node):
    if node.left.is_empty():
        return node.value
    return minimum(node.left)


def delete(node, value):
    if value < node.value:
        node.left = delete(node.left, value)
        return node
    if value == node.value:
        if node.left.is_empty():
            return node.right
        elif node.right.is_empty():
            return node.left
        else:
            node.value = minimum(node.right)
            node.right = delete(node.right, node.value)
            return node
    node.right = delete(node.right, value)
    return node


top = Node(5)
insert(top, 6)
insert(top, 8)
insert(top, 4)
insert(top, 3)
insert(top, 10)
insert(top, 7)
insert(top, 11)

show(top)

delete(top, 3)
show(top)

delete(top, 5)
show(top)
