class One(object):

    __slots__ = ()


class Two(One):

    __slots__ = ()


class Three(One):

    __slots__ = ()


class Four(Two, Three):

    __slots__ = ()


class Five(object):

    __slots__ = ("Foo", "Bar")


class Six(Five):

    __slots__ = ()


class Seven(Five):

    __slots__ = ()

try:
    class Eight(Five, Six):

        __slots__ = ()

except TypeError:
    print "Diamonds not allowed with slots"


class Nine(Five):

    __slots__ = ("Foo", "Alpha")


class Ten(object):

    __slots__ = ("Bar", "Beta")


try:
    class Eleven(Five, Ten):

        __slots__ = ()

except TypeError:
    print "Same slot in two parent"


class Twelve(object):

    __slots__ = ("X", "Y")

try:
    class Thirteen(Ten, Twelve):
        pass

except TypeError:
    print "Two different slots"


class Fourteen(object):

    __slots__ = ("Bar", "Beta", "X", "Y")


try:
    class Fifeteen(Fourteen, Ten):
        pass
except TypeError:
    print "slots in two parent"


class Sixteen(object):
    pass
    # NO slots

class Seventeen(Sixteen):

    __slots__ = ("name")

    def __init__(self):
        self.name = "Paul"
        self.other = 123

four = Four()
print four

nine = Nine()
print nine

seventeen = Seventeen()
print seventeen.other