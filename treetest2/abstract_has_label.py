from six import add_metaclass
from abc import abstractproperty

from abstract_base import AbstractBase

#@add_metaclass(AbstractBase)
class AbstractHasLabel(object):
    """ Represents an item with a label
    """

    __slots__ = ()

    def has_label(self):
        return True

    @abstractproperty
    def label(self):
        """ The label of the item

        :return: The label
        :rtype: str
        :raise None: Raises no known exceptions
        """
