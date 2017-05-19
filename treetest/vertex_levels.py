# from six import add_metaclass
# from abc import ABCMeta

from abstract_application_vertex import AbstractApplicationVertex


class VertexLevels(AbstractApplicationVertex):

    def label(self):
        return "hi"

    def add_constraint(self, constraint):
        pass

    def add_constraints(self, constraints):
        pass

    def constraints(self):
        return None
