from abstract_view import AbstractView


class ZoneView(AbstractView):

    __offset = None
    __length = None
    __range_dictionary = None

    def __init__(self,  range_dictionary, start, end):
        self.__range_dictionary = range_dictionary
        self.__offset = start
        self.__length = end - start

    def __iter__(self):
        return self.__range_dictionary.iter_by_zone(self.__start, self.__end)

    def __len__(self):
        return self.__range_dictionary.len_by_zone(self.__start, self.__end)

    def __getitem__(self, key):
        return self.__range_dictionary.getitem_by_zone(self.__start,
                                                       self.__end, key)

    def __setitem__(self, key, value):
        return self.__range_dictionary.setitem_by_zone(self.__start,
                                                       self.__end, key, value)

    def _check_range(self, start, end):
        if start < 0:
            raise Exception("Start must not be negative")
        if end < 0:
            raise Exception("End must not be negative")
        if start > end:
            raise Exception("Start must be less than or equal to end")
        if end > self.__length:
            raise Exception("End too high {} is greater than {}"
                            "".format(end, self.__length))

    def set_range(self, start, end, key, value):
        self._check_range(start, end)
        self.__range_dictionary.setitem_by_zone(start + self.__offset,
                                                end + self.__offset,
                                                key, value)

    def _check_index(self, index):
        if index < 0:
            raise Exception("Index must not be negative")
        if index > self.__length:
            raise Exception("Index too high {} is greater than {}"
                            "".format(index, self.__length))

    def set_value(self, index, key, value):
        self._check_index(index)
        self.__range_dictionary.setitem_by_zone(index + self.__offset, key,
                                                value)

    def get_by_index(self, index):
        self._check_index(index)
        return self.__range_dictionary.get_by_index(index + self.offset)

    def has_key(self, index, key):
        self._check_index(index)
        return (index + self.offset, key) in self.__range_dictionary

    def get_value(self, index, key):
        self._check_index(index)
        return self.__range_dictionary.get_value(index + self.offset, key)

    def get_view_by_index(self, index):
        self._check_index(index)
        return self.__range_dictionary.get_view_by_index(index + self.offset)
