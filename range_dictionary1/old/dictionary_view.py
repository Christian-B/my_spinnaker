import collections

class DictionaryView(collections.Mapping):

    __inner = None

    def __init__(self, inner):
        self.__inner = inner
        self._hash = None

    def __iter__(self):
        return iter(self.__inner)

    def __len__(self):
        return len(self.__inner)

    def __getitem__(self, key):
        return self.__inner[key]

    def __setitem__(self, key, value):
        self.__inner[key] = value

    def __hash__(self):
        # It would have been simpler and maybe more obvious to
        # use hash(tuple(sorted(self._d.iteritems()))) from this discussion
        # so far, but this solution is O(n). I don't know what kind of
        # n we are going to run into, but sometimes it's hard to resist the
        # urge to optimize when it will gain improved algorithmic performance.
        if self._hash is None:
            self._hash = 0
            for pair in self.iteritems():
                self._hash ^= hash(pair)
        return self._hash

    def __str__(self):
        return str(self.__inner)


class DictionaryWrapper(collections.Mapping):
    """Don't forget the docstrings!!"""

    __dictionary_view = None

    def __init__(self, dictionary_view, inner):
        self.__dictionary_view = dictionary_view

    @property
    def __inner(self):
        return self.__dictionary_view

    def __iter__(self):
        return iter(self.__inner)

    def __len__(self):
        return len(self.__inner)

    def __getitem__(self, key):
        return self.__inner[key]

    def __setitem__(self, key, value):
        self.__inner[key] = value


if __name__ == "__main__":
    inner = dict(a=1, b=2)
    setter = DictionaryView(inner)
    x = DictionaryWrapper(setter, inner)
    print x
    print x["a"]
    x["c"] = 4
    print x["c"]

    for a in x.iteritems():
        print a
