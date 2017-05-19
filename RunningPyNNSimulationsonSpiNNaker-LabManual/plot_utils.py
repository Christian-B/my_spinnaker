# Imports
import numpy as np
import matplotlib.pyplot as plt


def line_plot(v):
    print ("Setting up voltage line graph")
    neurons = np.unique(v[:, 0])
    for neuron in neurons:
        time = [i[1] for i in v if i[0] == neuron]
        membrane_voltage = [i[2] for i in v if i[0] == neuron]
        plt.plot(time, membrane_voltage)
    plt.xlabel("Time (ms)")
    plt.ylabel("Membrane Voltage")
    min_voltage = min(v[:, 2])
    max_voltage = max(v[:, 2])
    adjust = (max_voltage - min_voltage) * 0.1
    plt.axis([min(v[:, 1]), max(v[:, 1]), min_voltage - adjust,
              max_voltage + adjust])
    plt.show()


def heat_plot(v):
    print "Setting up volate heat graph"
    neurons = v[:, 0].astype(int)
    times = v[:, 1].astype(int)
    voltage = v[:, 2]
    voltage_array = np.nan * np.empty((max(neurons)+1, max(times)+1))
    voltage_array[neurons, times] = voltage
    plt.xlabel("Time (ms)")
    plt.ylabel("Neuron Id")
    plt.title("Voltage")
    plt.imshow(voltage_array, cmap='hot', interpolation='bilinear',
               aspect='auto')
    plt.colorbar()
    plt.show()


def plot_spikes(spikes, spikes2=None):
    found = False
    minTime = None
    maxTime = None
    minSpike = None
    maxSpike = None
    spike_time = [i[1] for i in spikes]
    spike_id = [i[0] for i in spikes]
    if len(spike_time) == 0:
        print "No spikes detected"
    else:
        found = True
        minTime = min(spike_time)
        maxTime = max(spike_time)
        minSpike = min(spike_id)
        maxSpike = max(spike_id)
        plt.plot(spike_time, spike_id, "b.",)
    if spikes2 is not None:
        spike_time = [i[1] for i in spikes2]
        spike_id = [i[0] for i in spikes2]
        if len(spike_time) == 0:
            print "No spikes detected in second spike data"
        else:
            found = True
            minTime = min(minTime, min(spike_time))
            maxTime = max(maxTime, max(spike_time))
            minSpike = min(minSpike, min(spike_id))
            maxSpike = max(maxSpike, max(spike_id))
            plt.plot(spike_time, spike_id, "r.", )
    if found:
        plt.xlabel("Time (ms)")
        plt.ylabel("Neuron ID")
        plt.title("spikes")
        timeDiff = (maxTime - minTime) * 0.05
        minTime = minTime - timeDiff
        maxTime = maxTime + timeDiff
        spikeDiff = (maxSpike - minSpike) * 0.05
        minSpike = minSpike - spikeDiff
        maxSpike = maxSpike + spikeDiff
        plt.axis([minTime, maxTime, minSpike, maxSpike])
        plt.show()


if __name__ == "__main__":
    v = np.load("v.npy")
    # line_plot(v)
    # heat_plot(v)
    spikes1 = np.load("pre_spikes.npy")
    spikes2 = np.load("post_spikes.npy")
    plot_spikes(spikes1, spikes2)
