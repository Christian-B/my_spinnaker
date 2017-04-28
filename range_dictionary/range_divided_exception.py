class RangeDividedException(Exception):


    def __init__(self, range_index):
        self._range_index = range_index

    def __str__(self):
        return "The range {} has been split bu a set call.".format(self._range_index)