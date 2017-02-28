try:
    import pyNN.spiNNaker as p
except:
    import spynnaker.pyNN as p

from pyNN.random import NumpyRNG, RandomDistribution

import plot_utils

import numpy

numpy.random.seed(1);

# Set up the simulation to use 0.1ms timesteps.
#p.setup(timestep=0.1)
p.setup(timestep=1)

# Choose the number of neurons to be simulated in the network.
num_neurons = 100

# Create an excitatory population with 80% of the neurons
# and an inhibitory population with 20% of the neurons.
ex_pop = p.Population(int(num_neurons * 0.8), p.IF_curr_exp, {},
                      label="excitatory population")
in_pop = p.Population(int(num_neurons * 0.2), p.IF_curr_exp, {},
                      label="inhibitory population")

# Create excitatory poisson stimulation population with 80% of the neurons
# and an inhibitory poisson stimulation population with 20% of the neurons,
# both with a rate of 1000Hz.
ex_pos = p.Population(int(num_neurons * 0.8),
                      p.SpikeSourcePoisson, {'rate': 100},
                      label="excitatory poisson")
in_pos = p.Population(int(num_neurons * 0.2),
                      p.SpikeSourcePoisson, {'rate': 100},
                      label="inhibitory poisson")

# Create a one-to-one excitatory connection
# from the excitatory poisson stimulation population
# to the excitatory population with a weight of 0.1nA and a delay of 1.0ms
ex_proj = p.Projection(ex_pos, ex_pop,
                       p.OneToOneConnector(weights=0.75, delays=1),
                       target="excitatory")

# Create a similar excitatory connection
# from the inhibitory poisson stimulation population
# to the inhibitory population.
in_proj = p.Projection(in_pos, in_pop,
                       p.OneToOneConnector(weights=0.75, delays=1),
                       target="excitatory")

# Create an excitatory connection from the excitatory population
# to the inhibitory population
# with a fixed probability of connection of 0.1,
# and using a normal distribution of weights with a mean of 0.1 (mu)
#   and standard deviation of 0.1 (sigma)
#   (remember to add a boundary to make the weights positive)
# and a normal distribution of delays with a mean of 1.5 (mu)
#   and standard deviation of 0.75 (sigma)
#   (remember to add a boundary to keep the delays
#       within the allowed range on SpiNNaker).
rd_weights = RandomDistribution('normal', [0.1, 0.1], boundaries=(0,100))
dist_weights = RandomDistribution('normal', [1.5, 0.75], boundaries=(0,100))
# ex_in_proj = p.Projection(ex_pop, in_pop,
#                          p.FixedProbabilityConnector(0.1, weights=rd_weights,
#                                                      delays=dist_weights),
#                          target="excitatory")


# Create a similar connection between the inhibitory population and itself.
in_in_proj = p.Projection(in_pop, in_pop,
                          p.FixedProbabilityConnector(0.1, weights=rd_weights,
                                                      delays=dist_weights),
                          target="excitatory")

# Initialize the membrane voltages of the excitatory and inhibitory populations
# to a uniform random number between -65.0 and -55.0.
rng = NumpyRNG(seed=1)
uniformDistr = RandomDistribution('uniform', [-65, -55], rng)
ex_pop.initialize('v', uniformDistr)
in_pop.initialize('v', uniformDistr)

# Record the spikes from the excitatory population.
ex_pop.record()
ex_pos.record()
# (and voltage)
ex_pop.record_v()

# Run the simulation for 1 or more seconds.
p.run(2000)

# Retrieve and plot the spikes.
v = ex_pop.get_v()
print v
numpy.save("v.npy", v)
numpy.savetxt("v.csv", v, fmt=['%d','%d','%s'], delimiter=',')
plot_utils.heat_plot(v)
#plot_utils.line_plot(v)

spikes = ex_pop.getSpikes()
print spikes
numpy.save("spikes", spikes)
numpy.savetxt("spikes.csv", spikes, fmt=['%d','%d'], delimiter=',')
plot_utils.plot_spikes(spikes)