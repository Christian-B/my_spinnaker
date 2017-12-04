import spynnaker8 as sim
import spynnaker8.spynnaker_plotting as splot
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt

simtime = 2000
n_neurons = 7
weight_to_spike = 5
delay = 5
RECEIVER_LABEL1 = "synfireOne"
RECEIVER_LABEL2 = "synfireTwo"
INJECTOR_LABEL = "injector"

# set up python live spike connection
live_spikes_connection = sim.external_devices.SpynnakerLiveSpikesConnection(
    receive_labels=[RECEIVER_LABEL1, RECEIVER_LABEL2],
    send_labels = [INJECTOR_LABEL])

# declare python code when received spikes for a timer tick
def receive_spikes(label, time, neuron_ids):
    for neuron_id in neuron_ids:
        print "Received spike at time {} from {}-{}" \
              "".format(time, label, neuron_id)
        if neuron_id + 1 == n_neurons:
            if label == RECEIVER_LABEL1:
                live_spikes_connection.send_spike(
                    INJECTOR_LABEL, 1, send_full_keys=True)
            else:
                live_spikes_connection.send_spike(
                    INJECTOR_LABEL, 0, send_full_keys=True)

# create python injector
def send_spike(label, sender):
    sender.send_spike(label, 0, send_full_keys=True)

# register python receiver with live spike connection
live_spikes_connection.add_receive_callback(RECEIVER_LABEL1, receive_spikes)
live_spikes_connection.add_receive_callback(RECEIVER_LABEL2, receive_spikes)

# register python injector with injector connection
live_spikes_connection.add_start_callback(INJECTOR_LABEL, send_spike)

sim.setup(timestep=1.0)

input = sim.Population(2, sim.external_devices.SpikeInjector(),
                       label=INJECTOR_LABEL)
synfire1 = sim.Population(n_neurons, sim.IF_curr_exp(tau_syn_E=5),
                          label=RECEIVER_LABEL1)
synfire2 = sim.Population(n_neurons, sim.IF_curr_exp(tau_syn_E=5),
                          label=RECEIVER_LABEL2)
sim.external_devices.activate_live_output_for(synfire1)
sim.external_devices.activate_live_output_for(synfire2)

loop_conns = list()
for i in range(0, n_neurons - 1):
    single_connection = (i, i + 1, weight_to_spike, delay)
    loop_conns.append(single_connection)
print loop_conns

input_proj = sim.Projection(input, synfire1, sim.OneToOneConnector(),
                            synapse_type=sim.StaticSynapse(weight=5, delay=1))
synfire1_proj = sim.Projection(synfire1, synfire1, sim.FromListConnector(loop_conns))
synfire2_proj = sim.Projection(synfire2, synfire2, sim.FromListConnector(loop_conns))

"""
s_neo = synfire1.get_data(variables=["spikes"])
spikes = s_neo.segments[0].spiketrains
print spikes
s_neo = synfire2.get_data(variables=["spikes"])
spikes = s_neo.segments[0].spiketrains
print spikes
"""

sim.run(simtime)

sim.end()

