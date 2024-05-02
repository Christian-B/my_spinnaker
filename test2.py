import time
import sys

class ChipA(tuple):

    def __new__(cls, x, y, t, r):
        return tuple.__new__(cls, (x, y))

    def __init__(self, x, y, t, r):
        self._t = t
        self._r = r

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def t(self):
        return self._t


class ChipB(object):

    __slots__ = ["_x", "_y", "_t", "_r"]

    def __init__(self, x, y, t, r):
        self._x = x
        self._y = y
        self._t = t
        self._r = r

    def __iter__(self):
       yield self._x
       yield self._y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def t(self):
        return self._t

    def __eq__(self, other):
        if isinstance(other, ChipB):
            return self._x == other._x and self._y == other._y
        else:
            return other == (self._x, self._y)

    def __hash__(self) -> int:
        return hash((self._x, self._y))

    def __getitem__(self, xy_id: int) -> int:
        """
         Allows the Chip to be used as an x, y tuple

         So
         chip[0] == chip.x   like (x,y)[0] == x
         chip[1] == chip.y   like (x,y)[1] == y

         :rtype: int
         """
        if xy_id == 0:
            return self._x
        if xy_id == 1:
            return self._y

start = time.time()
n = 10000
for _ in range(n):
    a = ChipB(1, 3, "bacon", 5)
    b = (1, 3)
    (x, y) = a
    assert a == b
    assert b == a
    assert hash(a) == hash(b)
    assert a.y == a[1]
    assert a.t == "bacon"
    assert a._r == 5
    l1 = [ChipB(1, 3, "bacon", 5), ChipB(3,5, "foo", 6)]
    l2 = [ChipB(1, 3, "bacon", 9), ChipB(3,5, "foo", 7)]
    l3 = [(1,3), (3,5)]
    assert l1==l2
    assert l2==l3
print(start-time.time())
print(sys.getsizeof(a))

start = time.time()
for _ in range(n):
    a = ChipA(1, 3, "bacon", 5)
    b = (1, 3)
    (x, y) = a
    assert a == b
    assert b == a
    assert hash(a) == hash(b)
    assert a.y == a[1]
    assert a.t == "bacon"
    assert a._r == 5
    l1 = [ChipA(1, 3, "bacon", 6), ChipA(3,5, "foo", 7)]
    l2 = [ChipA(1, 3, "bacon", 3), ChipA(3,5, "foo", 9)]
    l3 = [(1,3), (3,5)]
    assert l1==l2
    assert l2==l3
print(start-time.time())
print(sys.getsizeof(a))
