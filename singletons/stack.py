class Alpha(object):

    __singleton = None

    def __new__(cls):
        if cls.__singleton:
            return cls.__singleton
        # pylint: disable=protected-access
        obj = object.__new__(cls)
        cls.__singleton = obj
        obj._clear()
        return obj

    @staticmethod
    def foo():
        global __data
        print(__data)


class Beta(Alpha):

    __singleton = None

    def __new__(cls):
        if cls.__singleton:
            return cls.__singleton
        # pylint: disable=protected-access
        obj = object.__new__(cls)
        cls.__singleton = obj
        obj._clear()
        return obj

    @staticmethod
    def beta():
        global __data
        print(__data)

Beta.foo()