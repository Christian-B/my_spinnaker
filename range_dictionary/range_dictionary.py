from abstract_view import AbstractView

import copy

from mutliple_value_exception import MutlipleValueException
from range_divided_exception import RangeDividedException
from range_view import RangeView
from index_view import IndexView
from zone_view import ZoneView

class RangeDictionary(AbstractView):
    __data = dict()
    __keys_changed = False
    __start = None
    __end = None

    # Mapping method
    def __init__(self, start, end, default):
        self.__data[(start, end)] = default
        self.__start = start
        self.__end = end

    def __iter__(self):
        if self.__keys_changed:
            raise MutlipleValueException("__iter__")
        return iter(self.__data.values()[0])

    def __len__(self):
        if self.__keys_changed:
            raise MutlipleValueException("__len__")
        return len(self.__data.values()[0])

    def __getitem__(self, key):
        if self.__keys_changed:
            raise MutlipleValueException("__getitem__")
        return self.__data.values()[0][key]

    def __setitem__(self, key, value):
        if self.__keys_changed:
            self.setitem_by_zone(self.__start, self.__end, key, value)
        self.__data.values()[0][key] = value

    def get_ranges(self):
        return sorted(self.__data.keys())

    # index methods
    def iter_by_index(self, index):
        range_index = self.get_range_by_index(index)
        return self.iter_by_range(range_index)

    def len_by_index(self, index):
        range_index = self.get_range_by_index(index)
        return self.len_by_range(range_index)

    def getitem_by_index(self, index, key):
        range_index = self.get_range_by_index(index)
        return self.getitem_by_range(range_index, key)

    def setitem_by_index(self, index, key, value):
        range_index = self.get_range_by_index(index)
        self.setitem_by_range(range_index, key, value)

    def view_by_index(self, index):
        return IndexView(self, index)

    def get_range_by_index(self, index):
        for index_range in self.__data:
            if index <= index_range[1] and index >= index_range[0]:
                return index_range

    # range methods
    def iter_by_range(self, range_index):
        if self.__data.has_key(range_index):
            return iter(self.__data[range_index])
        raise RangeDividedException(range_index)

    def len_by_range(self, range_index):
        if self.__data.has_key(range_index):
            return len(self.__data[range_index])
        raise RangeDividedException(range_index)

    def getitem_by_range(self, range_index, key):
        if self.__data.has_key(range_index):
            return self.__data[range_index][key]
        raise RangeDividedException(range_index)

    def setitem_by_range(self, range_index, key, value):
        if self.__data.has_key(range_index):
            self.__data[range_index][key] = value
        raise RangeDividedException(range_index)

    def view_by_range(self, range_index):
        if self.__data.has_key(range_index):
            return RangeView(self, range_index)
        raise RangeDividedException(range_index)

    # zone methods
    def iter_by_zone(self, start, stop):
        ranges = self.get_ranges_by_zone(start, stop)
        if len(ranges) == 1:
            return iter(self.__data[ranges[0]])
        raise MutlipleValueException("__iter__")

    def len_by_zone(self, start, stop):
        ranges = self.get_ranges_by_zone(start, stop)
        if len(ranges) == 1:
            return len(self.__data[ranges[0]])
        raise MutlipleValueException("__iter__")

    def getitem__by_zone(self, start, stop, key):
        ranges = self.get_ranges_by_zone(start, stop)
        if len(ranges) == 1:
            return self.__data[ranges[0]][key]
        raise MutlipleValueException("__iter__")

    def setitem_by_zone(self, start, end, key, value):
        index_ranges = self.get_ranges_by_zone(start, end)
        # check if some of first range is kept rest a new range
        if start > index_ranges[0][0] and self._new_value(index_ranges[0], key, value):
            previous = self.__data[index_ranges[0]]
            previous_range = (index_ranges[0][0], start - 1)
            self.__data[previous_range] = previous
            del self.__data[index_ranges[0]]
            # make a clone in the overwrite part of first
            index_ranges[0] = (start, index_ranges[0][1])
            self.__data[index_ranges[0]] = copy.copy(previous)
        # check if some of last range is kept rest a new range
        if end < index_ranges[-1][1] and self._new_value(index_ranges[-1], key, value):
            previous = self.__data[index_ranges[-1]]
            previous_range = (end + 1, index_ranges[-1][1])
            self.__data[previous_range] = previous
            del self.__data[index_ranges[-1]]
            # make a clone in the overwrite part of the last
            index_ranges[-1] = (index_ranges[-1][0], end)
            self.__data[index_ranges[-1]] = copy.copy(previous)
        # update ranges
        for index_range in index_ranges:
            self.__data[index_range][key] = value

    def get_ranges_by_zone(self, start, end):
        self._check_range(start, end)
        results = []
        for index_range in self.__data:
            if start <= index_range[1] and end >= index_range[0]:
                results.append(index_range)
        return sorted(results)

    def view_by_zone(self, start, end):
        return ZoneView(self, start, end)

    # support methods
    def _check_range(self, start, end):
        if start > end:
            raise Exception("Start must be less than or equal to end")
        if start < self.__start:
            raise Exception("Start too low {} is less than {}".format(start, self.__start))
        if end > self.__end:
            raise Exception("Index too high {} is greater than {}".format(end, self.__end))

    def _check_index(self, index):
        if index < self.__start:
            raise Exception ("Index too low {} is less than {}".format(index, self.__start))
        if index > self.__end:
            raise Exception ("Index too high {} is greater than {}".format(index, self.__end))

    def _new_value(self, range_index, key, value):
        if self.__data.has_key(range_index):
            if self.__data[range_index].has_key(key):
                return not value == self.__data[range_index][key]
            else:
                return True
        raise Exception ("Ranges changed")
