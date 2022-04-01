import pyNN.spiNNaker as p

simtime = 2000
n_neurons = 7
weight_to_spike = 5
delay = 5
RECEIVER_LABEL = "synfire"
INJECTOR_LABEL = "injector"

# set up python live spike connection
live_spikes_connection = sim.external_devices.SpynnakerLiveSpikesConnection(
    receive_labels=[RECEIVER_LABEL], send_labels=[INJECTOR_LABEL])


# declare python code when received spikes for a timer tick
def receive_spikes(label, time, neuron_ids):
    for neuron_id in neuron_ids:
        print("Received spike at time {} from {}-{}"
              "".format(time, label, neuron_id))


# create python injector
def send_spike(label, sender):
    sender.send_spike(label, 0, send_full_keys=True)


# register python receiver with live spike connection
live_spikes_connection.add_receive_callback(RECEIVER_LABEL, receive_spikes)

# register python injector with injector connection
live_spikes_connection.add_start_callback(INJECTOR_LABEL, send_spike)

sim.setup(timestep=1.0)

input = sim.Population(1, sim.external_devices.SpikeInjector(),
                       label=INJECTOR_LABEL)
pop = sim.Population(n_neurons, sim.IF_curr_exp(tau_syn_E=5),
                     label=RECEIVER_LABEL)
sim.external_devices.activate_live_output_for(pop)

loop_conns = list()
for i in range(0, n_neurons - 1):
    single_connection = (i, i + 1, weight_to_spike, delay)
    loop_conns.append(single_connection)
single_connection = (n_neurons - 1, 0, weight_to_spike, delay)
loop_conns.append(single_connection)

input_proj = sim.Projection(input, pop, sim.OneToOneConnector(),
                            synapse_type=sim.StaticSynapse(weight=5, delay=2))
loop_proj = sim.Projection(pop, pop, sim.FromListConnector(loop_conns))

pop.record(["spikes"])
sim.run(simtime)

s_neo = pop.get_data(variables=["spikes"])
spikes = s_neo.segments[0].spiketrains
print(spikes)

sim.end()
