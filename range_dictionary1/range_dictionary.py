import collections
import copy

from range_view import RangeView as RangeView
from index_view import IndexView as SingleView
from zone_view import ZoneView


class RangeDictionary(collections.Mapping):

    __values = dict()
    __start = None
    __end = None

    def __init__(self, start, end, default):
        self.__values[(start, end)] = default
        self.__start = start
        self.__end = end

    # support methods

    def _new_value(self, index_range, key, value):
        if index_range in self.__values:
            if key in self.__values[index_range]:
                return not value == self.__values[index_range][key]
            else:
                return True
        raise Exception("Ranges changed")

    def _check_range(self, start, end):
        if start > end:
            raise Exception("Start must be less than or equal to end")
        if start < self.__start:
            raise Exception("Start too low {} is less than {}"
                            "".format(start, self.__start))
        if end > self.__end:
            raise Exception("Index too high {} is greater than {}"
                            "".format(end, self.__end))

    def _check_index(self, index):
        if index < self.__start:
            raise Exception("Index too low {} is less than {}"
                            "".format(index, self.__start))
        if index > self.__end:
            raise Exception("Index too high {} is greater than {}"
                            "".format(index, self.__end))

    # Mapping methods
    def __iter__(self):
        return iter(self.__values)

    def __len__(self):
        return len(self.__values)

    def __getitem__(self, key):
        return RangeView(self, key)

    # def __setitem__(self, key, value):
    #    self.__inner[key] = value

    def __str__(self):
        return str(self.__values)

    # range_index methods
    def iter_by_range(self, range_index):
        if range_index in self.__values:
            return iter(self.__values[range_index])
        raise Exception("Ranges changed")

    def len_by_range(self, range_index):
        if range_index in self.__values:
            return len(self.__values[range_index])
        raise Exception("Ranges changed")

    def getitem_by_range(self, range_index, key):
        if range_index in self.__values:
            return self.__values[range_index][key]
        raise Exception("Ranges changed")

    def setitem_by_range(self, range_index, key, value):
        if range_index in self.__values:
            self.__values[range_index][key] = value
        else:
            self.setitem_by_zone(range_index[0], range_index[1], key, value)

    def get_view_by_range(self, range_index):
        return self[range_index]

    # zone_index methods
    def get_ranges(self, start, end):
        self._check_range(start, end)
        results = []
        for index_range in self.all_get_ranges():
            if start <= index_range[1] and end >= index_range[0]:
                results.append(index_range)
        return sorted(results)

    def iter_by_zone(self, start, end):
        ranges = self.get_ranges(start, end)
        if len(ranges) > 0:
            raise Exception("Multiple Ranges")
        return iter(self.__values[ranges[0]])

    def len_by_zone(self, start, end):
        ranges = self.get_ranges()
        if len(ranges) > 0:
            raise Exception("Multiple Ranges")
        return len(self.__values[ranges[0]])

    def getitem_by_zone(self, start, end, key):
        ranges = self.get_ranges()
        if len(ranges) > 0:
            raise Exception("Multiple Ranges")
        return self.__values[ranges[0]][key]

    def setitem_by_zone(self, start, end, key, value):
        index_ranges = self.get_ranges(start, end)
        # check if some of first range is kept rest a new range
        if start > index_ranges[0][0] and \
                self._new_value(index_ranges[0], key, value):
            previous = self.__values[index_ranges[0]]
            previous_range = (index_ranges[0][0], start - 1)
            self.__values[previous_range] = previous
            del self.__values[index_ranges[0]]
            # make a clone in the overwrite part of first
            index_ranges[0] = (start, index_ranges[0][1])
            self.__values[index_ranges[0]] = copy.copy(previous)
        # check if some of last range is kept rest a new range
        if end < index_ranges[-1][1] and \
                self._new_value(index_ranges[-1], key, value):
            previous = self.__values[index_ranges[-1]]
            previous_range = (end + 1, index_ranges[-1][1])
            self.__values[previous_range] = previous
            del self.__values[index_ranges[-1]]
            # make a clone in the overwrite part of the last
            index_ranges[-1] = (index_ranges[-1][0], end)
            self.__values[index_ranges[-1]] = copy.copy(previous)
        # update ranges
        for index_range in index_ranges:
            self.__values[index_range][key] = value

    def get_view_by_zone(self, start, end):
        return ZoneView(self, start, end)

    # index methods
    def get_range(self, index):
        self._check_index(index)
        for (start, end) in self.all_get_ranges():
            if start <= index and end >= index:
                return (start, end)

    def iter_by_index(self, index):
        range_index = self.get_range(index)
        return iter(self.__values[range_index])

    def len_by_index(self, index):
        range_index = self.get_range(index)
        return len(self.__values[range_index])

    def getitem_by_index(self, index, key):
        range_index = self.get_range(index)
        return self.__values[range_index][key]

    def setitem_by_index(self, index, key, value):
        self.setitem_by_zone(index, index, key, value)

    def get_view_by_index(self, index):
        return SingleView(self, index)
