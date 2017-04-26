try:
    import pyNN.spiNNaker as p
except:
    import spynnaker.pyNN as p
import pylab

def plot_voltage(v):
    time = [i[1] for  i in v if  i[0] == 0]
    membrane_voltage = [i[2] for i in v if i[0] == 0]
    pylab.plot(time, membrane_voltage)
    pylab.xlabel("Time (ms)")
    pylab.ylabel("Membrane Voltage")
    pylab.axis([0, 10, -75, -45])
    pylab.show()

def plot_spikes(spikes):
    spike_time = [i[1] for i in spikes]
    spike_id = [i[0] for i in spikes]
    pylab.plot(spike_time, spike_id, ".")
    pylab.xlabel("Time (ms)")
    pylab.ylabel("Neuron ID")
    pylab.axis([0, 10, -1, 1])
    pylab.show()

p.setup(timestep=1)
pop_1 = p.Population(1, p.IF_curr_exp, {}, label="pop_1")
input=p.Population(1,p.SpikeSourceArray, {'spike_times': [[0]]}, label="input")
input_proj = p.Projection(input, pop_1, p.OneToOneConnector(weights=5.0, delays=1), target="excitatory")
pop_1.record()
pop_1.record_v()
p.run(10)
v = pop_1.get_v()
print v
spikes = pop_1.getSpikes()
print spikes
#plot_voltage(v)
#plot_spikes(spikes)
print "DONE"