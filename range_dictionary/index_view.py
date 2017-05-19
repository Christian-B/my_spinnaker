from abstract_view import AbstractView


class IndexView(AbstractView):

    __index = None
    __range_dictionary = None

    def __init__(self, range_dictionary, index):
        self.__index = index
        self.__range_dictionary = range_dictionary

    def __iter__(self):
        return self.__range_dictionary.iter_by_index(self.__index)

    def __len__(self):
        return self.__range_dictionary.len_by_index(self.__index)

    def __getitem__(self, key):
        return self.__range_dictionary.getitem_by_index(self.__index, key)

    def __setitem__(self, key, value):
        return self.__range_dictionary.setitem_by_index(self.__index,
                                                        key, value)

    def get_index(self):
        return self.__index

    def __str__(self):
        return str(self.__index) + ": " + self.data_string()
