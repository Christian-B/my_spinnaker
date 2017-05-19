import collections


class RangeView(collections.Mapping):

    __range_dictionary = None
    __range_index = None

    def __init__(self, range_dictionary, range_index):
        self.___range_dictionary = range_dictionary
        self.___range_index = range_index

    def __iter__(self):
        return self.___range_dictionary.iter_by_range(self.___range_index)

    def __len__(self):
        return self.___range_dictionary.len_by_range(self.___range_index)

    def __getitem__(self, key):
        return self.___range_dictionary.getitem_by_range(self.___range_index,
                                                         key)

    def __setitem__(self, key, value):
        return self.___range_dictionary.setitem_by_range(self.___range_index,
                                                         key, value)
