class Empty(object):

    __slots__ = ("max_length")

    def __init__(self):
        self.max_length = 0

    def show(self, level, tab=""):
        return

    def is_empty(self):
        return True

    def has_value(self, value):
        return False

    def __len__(self):
        return 0

    def balanced(self):
        return True

    def __iter__(self):
        return self

    def next(self):
        raise StopIteration()
