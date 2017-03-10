from six import add_metaclass

from abstract_base import AbstractBase, abstractmethod, abstractproperty

@add_metaclass(AbstractBase)
class AbstractHasConstraints(object):
    """ Represents an object with constraints
    """

    __slots__ = ()

    def __newX__(mcls, name, bases, namespace):
        cls = super(AbstractHasConstraints, mcls).__new__(mcls, name, bases,
                                                          namespace)

        abstracts = set(name for name, value in namespace.items() if
                        getattr(value, "__isabstractmethod__", False))
        for base in bases:
            for name in getattr(base, "__abstractmethods__", set()):
                value = getattr(cls, name, None)
                if getattr(value, "__isabstractmethod__", False):
                   abstracts.add(name)
        cls.__abstractmethods__ = frozenset(abstracts)
        return cls

    @abstractmethod
    def add_constraint(self, constraint):
        """ Add a new constraint to the collection of constraints

        :param constraint: constraint to add
        :type constraint:\
                    :py:class:`pacman.model.constraints.abstract_constraint.AbstractConstraint`
        :return: None
        :rtype: None
        :raise pacman.exceptions.PacmanInvalidParameterException: If the\
                    constraint is not valid
        """

    @abstractmethod
    def add_constraints(self, constraints):
        """ Add an iterable of constraints to the collection of constraints

        :param constraints: iterable of constraints to add
        :type constraints: iterable of\
                    :py:class:`pacman.model.constraints.abstract_constraint.AbstractConstraint`
        :return: None
        :rtype: None
        :raise pacman.exceptions.PacmanInvalidParameterException: If one of \
                    the constraints is not valid
        """

    @abstractproperty
    def constraints(self):
        """ An iterable of constraints

        :return: iterable of constraints
        :rtype: iterable of\
                    :py:class:`pacman.model.constraints.abstract_constraint\
                    .AbstractConstraint`
        :raise None: Raises no known exceptions
        """
