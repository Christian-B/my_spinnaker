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

four = Four()
print four

nine = Nine()
print nine
