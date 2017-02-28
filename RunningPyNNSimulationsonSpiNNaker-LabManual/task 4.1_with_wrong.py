try:
    import pyNN.spiNNaker as p
except:
    import spynnaker.pyNN as p

import plot_utils

import numpy

# Write a network with a 1.0ms time step
p.setup(timestep=1)
num_neurons = 10 # must be even
# consisting of two single-neuron populations
pre_pop = p.Population(num_neurons, p.IF_curr_exp, {},
                       label="pre population")
post_pop = p.Population(num_neurons, p.IF_curr_exp, {},
                        label="post population")
pre_pop.record()
post_pop.record()

# connected with an STDP synapse using a spike pair rule and
# additive weight dependency, and initial weights of 0.
timing_rule = p.SpikePairRule(tau_plus=20.0, tau_minus=20.0)
weight_rule = p.AdditiveWeightDependence(w_max=5.0, w_min=0.0, A_plus=0.5,
                                         A_minus=0.5)
stdp_model = p.STDPMechanism(timing_dependence=timing_rule,
                             weight_dependence=weight_rule)
stdp_projection = p.Projection(pre_pop, post_pop,
                               p.OneToOneConnector(weights=0.0, delays=5.0),
synapse_dynamics=p.SynapseDynamics(slow=stdp_model))

# Stimulate each of the neurons with a spike source array
# with times of your choice,
train_pos = p.Population(num_neurons,
                         p.SpikeSourcePoisson, {'rate': 10},
                         label="training poisson")

# with the times for stimulating the first neuron being slightly before
# the times stimulating the second neuron (e.g. 2ms or more),
# ensuring the times are far enough apart not to cause depression
# (compare the spacing in time with the
# tau_plus and tau_minus settings);
# note that a weight of 5.0 should be enough to force an IF_curr_exp neuron
# to fire with the default parameters.
pre_proj = p.Projection(train_pos, pre_pop,
                        p.OneToOneConnector(weights=5, delays=0),
                        target="excitatory")

loopConnections = list()
weight_to_spike = 5.0
delay = 3
for i in range(0, num_neurons/2):
    singleConnection = (i, i, weight_to_spike, delay)
    loopConnections.append(singleConnection)
for i in range(num_neurons/2,  num_neurons-1):
    singleConnection = (i, i+1, weight_to_spike, delay)
    loopConnections.append(singleConnection)
singleConnection = (num_neurons-1, num_neurons/2, weight_to_spike, delay)
loopConnections.append(singleConnection)
loop_proj = p.Projection(train_pos, post_pop,
                         p.FromListConnector(loopConnections),
                         target="excitatory")


# Add a few extra times at the end of the run for stimulating the first neuron.
# Run the network for a number of milliseconds and
p.run(2000)

# extract the spike times of the neurons and the weights.
pre_spikes = pre_pop.getSpikes()
numpy.save("pre_spikes", pre_spikes)
numpy.savetxt("pre_spikes.csv", pre_spikes, fmt=['%d','%d'], delimiter=',')

post_spikes = post_pop.getSpikes()
numpy.save("post_spikes", post_spikes)
numpy.savetxt("post_spikes.csv", post_spikes, fmt=['%d','%d'], delimiter=',')

plot_utils.plot_spikes(pre_spikes, post_spikes)

weights = stdp_projection.getWeights()
print weights
numpy.save("weights", weights)
numpy.savetxt("weights.csv", weights, delimiter=',')