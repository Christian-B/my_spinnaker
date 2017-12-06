import spynnaker8 as p

INJECTOR_LABEL = "injector"
RECEIVER_LABEL = "receiver"


# declare python code when received spikes for a timer tick
def receive_spikes(label, time, neuron_ids):
    for neuron_id in neuron_ids:
        print "Received spike at time {} from {}-{}" \
              "".format(time, label, neuron_id)


p.setup(timestep=1.0)
p1 = p.Population(1, p.IF_curr_exp(), label="pop_1")
input_injector = p.Population(1, p.external_devices.SpikeInjector(),
                              label=INJECTOR_LABEL)
# set up python live spike connection
live_spikes_connection = p.external_devices.SpynnakerLiveSpikesConnection(
    receive_labels=[RECEIVER_LABEL])

# register python receiver with live spike connection
live_spikes_connection.add_receive_callback(RECEIVER_LABEL, receive_spikes)


input_proj = p.Projection(input, p1, p.OneToOneConnector(),
                          p.StaticSynapse(weight=5, delay=3))
p1.record(["spikes", "v"])

p.run(50)

neo = p1.get_data(["spikes", "v"])
spikes = neo.segments[0].spiketrains
print spikes
v = neo.segments[0].filter(name='v')[0]
print v
