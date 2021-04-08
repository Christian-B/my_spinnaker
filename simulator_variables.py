try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping
from operator import attrgetter

_singleton = None


class CustomProperty(object):
    def __init__(self, attr):
        self.attr = attr

    def __get__(self, ins, type):
        print('inside __get__')
        if ins is None:
            pop = 1/0
            return self
        else:
            return attrgetter(self.attr)(ins)

    def __set__(self, ins, value):
        print('inside __set__')
        head, tail = self.attr.rsplit('.', 1)
        obj = attrgetter(head)(ins)
        setattr(obj, tail, value)


class SimulatorVariables(Mapping):
    __storage = {}
    __loaded = False

    def __new__(cls):
        global _singleton
        if _singleton:
            return _singleton
        _singleton = super(SimulatorVariables, cls).__new__(cls)
        return _singleton

    def __getitem__(self, item):
        return self.__storage.get(item)

    def __iter__(self):
        return iter(self.__storage)

    def __len__(self):
        return len(self.__storage)

    def load(self, **kwargs):
        if self.__loaded:
            raise Exception("No reload allowed Sucker!")
        for key, value in kwargs.items():
            self.__storage[key] = value
            setattr(self, key, value)
        self.__loaded = True

    def __setattr__(self, *args, **kwargs):
        if self.__loaded:
            raise Exception("Nice try Sucker!")
        object.__setattr__(self, *args, **kwargs)


if __name__ == '__main__':
    sim = SimulatorVariables()
    sim.load(foo=1, bar=2)
    print(sim)
    sim2 = SimulatorVariables()
    print(sim2)
    print(list(sim2.items()))
    print(sim2.foo)
    print(sim2.bar)
    sim.__dict__["foo"] = 12
    print(sim2.foo)