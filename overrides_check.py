from six import add_metaclass
from spinn_utilities.abstract_base import (
    abstractmethod, abstractproperty, AbstractBase)
from spinn_utilities.overrides import overrides

@add_metaclass(AbstractBase)
class AbstractBacon(object):

    @abstractmethod
    def __init__(self, foo, bar):
        """

        :param foo:
        :param bar:
        :return:
        """

    @abstractmethod
    def eat(self, slices):
        """

        :param slices:
        :return:
        """

class MeatBacon(AbstractBacon):

    def __init__(self, foo, bar):
        print(bar, foo)

    def eat(self, slices):
        print("Yumm")

class VegiBacon(AbstractBacon):

    #@overrides(AbstractBacon.__init__)
    def __initX__(self, gamma, bar, burp):
        print(bar, gamma)

    @overrides(AbstractBacon.eat)
    def eats(self, slices, boo):
        print("Yumm")

m = MeatBacon(1, 2 )
v = VegiBacon()