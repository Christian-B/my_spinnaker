class MutlipleValueException(Exception):

    def __init__(self, method):
        self._method = method

    def __str__(self):
        return "The method {} would return more than one value.".format(method)