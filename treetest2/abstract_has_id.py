from six import add_metaclass
from abc import abstractproperty

from abstract_base import AbstractBase

#@add_metaclass(AbstractBase)
class AbstractHasId(object):
    """ Represents an item with a label
    """

    __slots__ = ()

    @abstractproperty
    def id(self):
        """ The label of the item

        :return: The label
        :rtype: str
        :raise None: Raises no known exceptions
        """
