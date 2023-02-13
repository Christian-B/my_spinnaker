class FecDataModel(object):

    __singleton = None

    __slots__ = ["__foo", "__bar"]

    def __new__(cls):
        if cls.__singleton:
            return cls.__singleton
        # pylint: disable=protected-access
        obj = object.__new__(cls)
        cls.__singleton = obj
        obj.clear()
        return obj

    def clear(self):
        self.__foo = None
        self.__bar = None


class FecDataView(object):

    __fec_data = FecDataModel()

    @property
    def foo(self):
        if self.__fec_data._FecDataModel__foo is None:
            raise NotImplementedError
        return self.__fec_data._FecDataModel__foo

    def has_foo(self):
        return self.__fec_data._FecDataModel__foo is not None


class FecDataSetter(FecDataView):

    def set_foo(self, new_value):
        self._fec_data._FecDataModel__foo = new_value


class SpyDataModel(object):

    __singleton = None

    __slots__ = ["__alpha", "__beta"]

    def __new__(cls):
        if cls.__singleton:
            return cls.__singleton
        # pylint: disable=protected-access
        obj = object.__new__(cls)
        cls.__singleton = obj
        obj.clear()
        return obj

    def clear(self):
        self.__alpha = None
        self.__beta = None


class SpyDataView(FecDataView):

    _spy_data = SpyDataModel()

    @property
    def alpha(self):
        if self._spy_data._SpyDataModel__foo is None:
            raise NotImplementedError
        return self._spy_data._SpyDataModel__foo


class SpyDataSetter(SpyDataView, FecDataSetter):

    def __init__(self):
        SpyDataView.__init__(self)
        FecDataSetter.__init__(self)

    def set_alpha(self, new_value):
        self._spy_data._SpyDataModel__alpha = new_value


v = FecDataView()
s = FecDataSetter()
v2 = SpyDataView()
s2 = SpyDataSetter()
print(v2.has_foo())
s.set_foo(12)
print(v.foo)
print(s.foo)
print(v2.foo)
print(s2.foo)
s2.set_foo(13)
print(v.foo)
print(s.foo)
print(v2.foo)
print(s2.foo)
