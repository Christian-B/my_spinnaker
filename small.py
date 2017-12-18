import spynnaker8 as sim
# import pyNN.utility.plotting as plot
# import matplotlib.pyplot as plt

sim.setup(timestep=1)
sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 100)

pop_1 = sim.Population(15, sim.IF_curr_exp(), label="pop_1")
input = sim.Population(1, sim.SpikeSourceArray(spike_times=[0]), label="input")
# input_proj = sim.Projection(input, pop_1, sim.AllToAllConnector(),
#                            synapse_type=sim.StaticSynapse(weight=5, delay=1))
loop_conns = list()
for i in range(0, 15, 4):
    single_connection = (0, i)
    loop_conns.append(single_connection)
print loop_conns
input_proj = sim.Projection(input, pop_1, sim.FromListConnector(loop_conns),
                            synapse_type=sim.StaticSynapse(weight=5, delay=1))
pop_1.record("spikes")
# pop_1.record("v", sampling_interval=2)
simtime = 10
sim.run(simtime)
neo = pop_1.get_data()
# pop_2 = sim.Population(5, sim.IF_curr_exp(), label="pop_2")
# sim.reset()
# sim.run(simtime)

# neo = pop_1.get_data(variables=["spikes", "v"])
spikes = neo.segments[0].spiketrains
print spikes
print len(spikes)
# spikes = neo.segments[1].spiketrains
# print spikes
# print len(spikes)
# print spikes[0].sampling_rate
# v = neo.segments[0].filter(name='v')[0]
# print v
# v = neo.segments[1].filter(name='v')[0]
# print v
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
