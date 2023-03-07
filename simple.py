# Copyright 2017-2023 The University of Manchester
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt
import pyNN.spiNNaker as sim

sim.setup(timestep=1.0)

sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 50)
pop_1 = sim.Population(500, sim.IF_curr_exp(), label="pop_1")
pop_1.set_max_atoms_per_core(500)
input = sim.Population(500, sim.SpikeSourceArray(spike_times=[0]), label="input")
input_proj = sim.Projection(input, pop_1, sim.OneToOneConnector(),
                            synapse_type=sim.StaticSynapse(weight=5, delay=1))
pop_1.record(["spikes", "v"])
simtime = 10
sim.run(simtime)


neo = pop_1.get_data(variables=["spikes", "v"])
spikes = neo.segments[0].spiketrains
print(spikes)
v = neo.segments[0].filter(name='v')[0]
print(v)
sim.end()

plt.show()
