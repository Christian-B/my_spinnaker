import collections


class AbstractView(collections.Mapping):

    def has_key(self, key):
        return key in iter(self)

    def data_string(self):
        result = "{"
        for (key, value) in self.items():
            result += str(key) + ":" + str(value) + ","
        return result[:-1] + "}"
