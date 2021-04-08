from pyNN.common import Population, Assembly, PopulationView
from pyNN.models import BaseCellType


class MockPopulation(Population):

    def __init__(self, size, cellclass, label):
        self._simulator = "mock"
        super(MockPopulation, self).__init__(size=size, cellclass=cellclass, label=label)

    def _recorder_class(self, myself):
        return "bacon"

    def _create_cells(self):
        self.all_cells = list(range(self.size))

    def _assembly_class(self, pop1, pop2):
        return MockAssembly(pop1, pop2)


class MockAssembly(Assembly):

    def __init__(self, *populations):
        self._simulator = "mock"
        super(MockAssembly, self).__init__(*populations)


class MockView(PopulationView):

    def __init__(self, parent, selector, label=None):
        self._simulator = "mock"
        super(MockView, self).__init__(parent=parent, selector=selector, label=label)


p1 = MockPopulation(size=5, cellclass=BaseCellType(), label="p1")
p2 = MockPopulation(size=5, cellclass=BaseCellType(), label="p2")

a1 = p1 + p2

v1 = MockView(parent=p1, selector = slice(2), label = "v1")

a1._insert(v1)