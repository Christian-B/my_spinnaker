# Imports
import numpy as np
import matplotlib.pyplot as plt

def line_plot(v):
    print ("Setting up voltage line graph")
    neurons = np.unique(v[:, 0])
    for neuron in neurons:
        time = [i[1] for  i in v if  i[0] == neuron]
        membrane_voltage = [i[2] for i in v if i[0] == neuron]
        plt.plot(time, membrane_voltage)
    plt.xlabel("Time (ms)")
    plt.ylabel("Membrane Voltage")
    min_voltage = min(v[:,2])
    max_voltage = max(v[:,2])
    adjust =  (max_voltage -  min_voltage) * 0.1
    plt.axis([min(v[:,1]), max(v[:,1]), min_voltage - adjust, max_voltage + adjust])
    plt.show()

def heat_plot(v):
    print "Setting up volate heat graph"
    neurons = v[:, 0].astype(int)
    times = v[:, 1].astype(int)
    voltage = v[:, 2]
    voltage_array = np.nan * np.empty((max(neurons)+1,max(times)+1))
    voltage_array[neurons, times] = voltage
    plt.xlabel("Time (ms)")
    plt.ylabel("Neuron Id")
    plt.title("Voltage");
    plt.imshow(voltage_array, cmap='hot', interpolation='bilinear', aspect='auto')
    plt.colorbar()
    plt.show()

def plot_spikes(spikes):
    spike_time = [i[1] for i in spikes]
    spike_id = [i[0] for i in spikes]
    plt.plot(spike_time, spike_id, ".")
    plt.xlabel("Time (ms)")
    plt.ylabel("Neuron ID")
    plt.title("spikes");
    plt.axis([min(spike_time), max(spike_time), min(spike_id), max(spike_id)])
    plt.show()


if __name__ == "__main__":
    v = np.load("v.npy")
    line_plot(v)
    heat_plot(v)
    ## spikes = np.load("spikes.npy")
    # print spikes
    # plot_spikes(spikes);

# plot_voltage(v)

# a = np.random.random((16, 16))
# print a
# plt.imshow(a, cmap='hot', interpolation='nearest')
# plt.show()

"""
#here's our data to plot, all normal Python lists
x = [1, 2, 3, 4, 5]
y = [0.1, 0.2, 0.3, 0.4, 0.5]

intensity = [
    [5, 10, 15, 20, 25],
    [30, 35, 40, 45, 50],
    [55, 60, 65, 70, 75],
    [80, 85, 90, 95, 100],
    [105, 110, 115, 120, 125]
]

print "x"
print x
print "y"
print y
print "intensity"
print intensity

#setup the 2D grid with Numpy
x, y = np.meshgrid(x, y)

#convert intensity (list of lists) to a numpy array for plotting
intensity = np.array(intensity)

print "x"
print x
print "y"
print y
print "intensity"
print intensity


#now just plug the data into pcolormesh, it's that easy!
plt.pcolormesh(x, y, intensity)
# plt.pcolormesh(v)
plt.colorbar() #need a colorbar to show the intensity scale
plt.show() #boom
"""