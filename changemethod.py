
class Number(object):

    def __init__(self, value):
        if value % 2 != 0:
            self.even = self._odds_even
        else:
            self.even = self._even

    def _even(self):
        print("even")
        return True

    def _odds_even(self):
        print("not odd")
        return False


a = Number(2)
a.even()
b = Number(3)
b.even()
a.even()
