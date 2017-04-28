import copy

class RangeDictionary():

    __values = dict()
    __start = None
    __end = None

    def __init__(self, start, end, default):
        self.__values[(start, end)]= default
        self.__start = start
        self.__end = end

    def set_range(self, start, end, value):
        index_ranges = self.get_ranges(start, end)
        # check if some of first range is kept
        if start > index_ranges[0][0]:
            print index_ranges[0]
            previous = self.__values[index_ranges[0]]
            previous_range = (index_ranges[0][0], start - 1)
            self.__values[previous_range] = previous
        # check if some of last range is kept
        if end < index_ranges[-1][1]:
            previous = self.__values[index_ranges[-1]]
            previous_range = (end + 1, index_ranges[-1][1])
            self.__values[previous_range] = previous
        # remove previous ranges
        for previous_range in index_ranges:
            del self.__values[previous_range]
        self.__values[(start, end)] = value

    def all_get_ranges(self):
        return sorted(self.__values.keys())

    def get_ranges(self, start, end):
        if start > end:
            raise Exception ("Start must be less than or equal to end")
        if start < self.__start:
            raise Exception ("Start too low {} is less than {}".format(start, self.__start))
        if end > self.__end:
            raise Exception ("Index too high {} is greater than {}".format(end, self.__end))
        results = []
        for index_range in self.all_get_ranges():
            if start <= index_range[1] and end >= index_range[0]:
                results.append(index_range)
        return sorted(results)

    def get_range(self, index):
        if index < self.__start:
            raise Exception ("Index too low {} is less than {}".format(index, self.__start))
        if index > self.__end:
            raise Exception ("Index too high {} is greater than {}".format(index, self.__end))
        for (start, end) in self.all_get_ranges():
            if start <= index and end >= index:
                return (start, end)

    def get_by_range(self, index_range):
        if self.__values.has_key(index_range):
            return copy.copy(self.__values[index_range])
        raise Exception ("Ranges changed")

    def get_by_value(self, index):
        index_range = self.get_range(index)
        return self.get_by_range(index_range)