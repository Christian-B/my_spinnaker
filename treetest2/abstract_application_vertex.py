from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty

from six import add_metaclass

from abstract_vertex import AbstractVertex


class AbstractApplicationVertex(AbstractVertex):
    """ A vertex that can be broken down into a number of smaller vertices\
        based on the resources that the vertex requires
    """

    __slots__ = ()

