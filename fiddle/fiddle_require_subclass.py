from pacman.model.graphs.machine import MachineVertex
from spinn_front_end_common.abstract_models import (
    AbstractGeneratesDataSpecification, AbstractSupportsBitFieldGeneration,
    AbstractSupportsBitFieldRoutingCompression)


class SideClass(
        AbstractSupportsBitFieldGeneration,
        AbstractSupportsBitFieldRoutingCompression,
        allow_derivation=True):

    def read_parameters_from_machine(
            self, transceiver, placement, vertex_slice):
        pass


class TopClass(MachineVertex):
    @property
    def resources_required(self):
        pass


class JoinClass(TopClass, SideClass, AbstractGeneratesDataSpecification):
    def generate_data_specification(self, spec, placement):
        pass


#a = JoinClass()
