from six import add_metaclass
from abc import ABCMeta

from abstract_has_constraints \
    import AbstractHasConstraints
from abstract_has_label \
    import AbstractHasLabel


@add_metaclass(ABCMeta)
class AbstractVertex(AbstractHasConstraints, AbstractHasLabel):
    """ A vertex in a graph
    """

    __slots__ = ()
