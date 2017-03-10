from six import add_metaclass


from abstract_has_constraints \
    import AbstractHasConstraints
from abstract_has_label \
    import AbstractHasLabel


class AbstractVertex(AbstractHasConstraints, AbstractHasLabel):
    """ A vertex in a graph
    """

    __slots__ = ()
