from abstract_view import AbstractView


class RangeView(AbstractView):

    __range_dictionary = None
    __range_index = None

    def __init__(self, range_dictionary, range_index):
        self.__range_dictionary = range_dictionary
        self.__range_index = range_index

    def __iter__(self):
        return self.__range_dictionary.iter_by_range(self.__range_index)

    def __len__(self):
        return self.__range_dictionary.len_by_range(self.__range_index)

    def __getitem__(self, key):
        return self.__range_dictionary.getitem_by_range(self.__range_index,
                                                        key)

    def __setitem__(self, key, value):
        return self.__range_dictionary.setitem_by_range(self.__range_index,
                                                        key, value)

    def __str__(self):
        return str(self.__range_index) + self.data_string()

    def __repr__(self):
        return str(self)
