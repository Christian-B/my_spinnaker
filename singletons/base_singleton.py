class BaseSingleton(object):

    __singleton = None

    def __new__(cls):
        if cls.__singleton:
            return cls.__singleton
        # pylint: disable=protected-access
        obj = object.__new__(cls)
        cls.__singleton = obj
        return obj

class LevelTwoSingleton(BaseSingleton):
    pass

print("here")
s1 = BaseSingleton()
s2 = LevelTwoSingleton()
print(id(s1))
print(id(s2))
