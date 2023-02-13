# Copyright (c) 2017-2020 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# fluff

import matplotlib.pyplot as pylab
import numpy
from pyNN.random import RandomDistribution
from pyNN.utility.plotting import Figure, Panel
import pyNN.spiNNaker as p

p.setup(timestep=0.1)
p.set_number_of_neurons_per_core(p.IF_curr_exp, 64)
p.set_number_of_neurons_per_core(p.SpikeSourcePoisson, 64)
n_neurons = 500