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

import spynnaker8 as sim
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt

sim.setup(timestep=1.0)

n_neurons = 1 # 75 works 76 fails

pop_1 = sim.Population(n_neurons, sim.IF_curr_exp(), label="pop_1")
input1 = sim.Population(
    n_neurons, sim.SpikeSourceArray(spike_times=range(0, 1000, 100)),
    label="input")
sim.Projection(
    input1, pop_1, sim.OneToOneConnector(),
    synapse_type=sim.StaticSynapse(weight=5, delay=80))

#input_proj = sim.Projection(input, pop_1, sim.OneToOneConnector(),
#                            synapse_type=sim.StaticSynapse(weight=5, delay=80))
pop_1.record(["spikes", "v"])
simtime = 1200
sim.run(simtime)

neo = pop_1.get_data(variables=["spikes", "v"])
# spikes = neo.segments[0].spiketrains
spikes = pop_1.spinnaker_get_data("spikes")

print(spikes)
v = neo.segments[0].filter(name='v')[0]
#print(v)
sim.end()
"""
plot.Figure(
    # plot voltage for first ([0]) neuron
    plot.Panel(v, ylabel="Membrane potential (mV)",
               data_labels=[pop_1.label], yticks=True, xlim=(0, simtime)),
    # plot spikes (or in this case spike)
    plot.Panel(spikes, yticks=True, markersize=5, xlim=(0, simtime)),
    title="Simple Example",
    annotations="Simulated with {}".format(sim.name())
)
plt.show()
"""