try:
    import pyNN.spiNNaker as p
except:
    import spynnaker.pyNN as p
import plot_utils

import logging
import numpy
import random

logger = logging.getLogger(__name__)

# Set up the simulation to use 0.1ms timesteps.
p.setup(timestep=1.0)
logger.info("CYB setup done")

# Create an input population of 1 source spiking at 0.0ms
input=p.Population(1,p.SpikeSourceArray, {'spike_times': [[0]]}, label="input")
logger.info("CYB input done")

# Create a synfire population with 100 neurons
nNeurons = 10
synfire_1 = p.Population(nNeurons, p.IF_curr_exp, {}, label="synfire_1")
logger.info("cyb synfire input done")

# With a FromListConnector, connect the input population to the first neuron of the synfire population,
# with a weight of 5nA and a delay of 1ms.
loopConnections = list()
weight_to_spike = 5.0
delay = 1
singleConnection = (0, 0, weight_to_spike, delay)
loopConnections.append(singleConnection)
input_proj = p.Projection(input, synfire_1, p.FromListConnector(loopConnections))

# Using another FromListConnector, connect each neuron in the synfire population to the next
# neuron, with a weight of 5nA and a delay of 5ms.
loopConnections = list()
weight_to_spike = 5.0
delay = 10
for i in range(0, nNeurons):
    singleConnection = (i, i+1, weight_to_spike, delay)
    loopConnections.append(singleConnection)
loop_proj = p.Projection(synfire_1, synfire_1, p.FromListConnector(loopConnections))

# Connect the last neuron in the synfire population to the first
loopConnections = list()
weight_to_spike = 5.0
delay = 5
singleConnection = (nNeurons-1, 0, weight_to_spike, delay)
loopConnections.append(singleConnection)
back_proj = p.Projection(synfire_1, synfire_1, p.FromListConnector(loopConnections))

logger.info("cyb connections done")

# Record the spikes produced from the synfire populations.
synfire_1.record()
synfire_1.record_v()

logger.info("CYB run start")
# Run the simulation for 2 seconds, and then retrieve and plot the spikes from the synfire population
p.run(2000)
logger.info("CYB run done")

v = synfire_1.get_v()
numpy.save("v.npy", v)
numpy.savetxt("v.csv", v, fmt=['%d','%d','%s'], delimiter=',')
plot_utils.heat_plot(v)

spikes = synfire_1.getSpikes()
numpy.save("spikes", spikes)
numpy.savetxt("spikes.csv", spikes, fmt=['%d','%d'], delimiter=',')
plot_utils.plot_spikes(spikes)