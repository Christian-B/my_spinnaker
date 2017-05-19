import collections


class IndexView(collections.Mapping):

    __index = None
    __range_dictionary = None

    def __init__(self, range_dictiorary, index):
        self.__index = index
        self.__range_dictionary = range_dictiorary

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

    def get_index(self):
        return self.__index

    def get_value(self, key):
        return self.__range_dictionary.get_value(self.__index, key)

    def set_value(self, key, value):
        self.__range_dictionary.setitem_by_index(self.__index, key, value)
