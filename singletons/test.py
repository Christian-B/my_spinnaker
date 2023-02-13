class View(object):

    __slots__ = ["__data"]

    def __init__(self):
        self.__data = 1

    def foo(self):
        print(self.__data)

    @property
    def num(self):
        return 1


class Writer(View):

    __slots__ = ["__data"]

    def __init__(self):
        View.__init__(self)
        self.__data = 2

    def bar(self):
        print(self.__data)

    @property
    def num(self):
        return 2


w = Writer()
w.foo()
w.bar()
print(w.num)