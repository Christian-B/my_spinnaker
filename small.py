import pyNN.spiNNaker as sim
# import pyNN.utility.plotting as plot
# import matplotlib.pyplot as plt

sim.setup(timestep=1.0)
pop_1 = sim.Population(1, sim.IF_curr_exp(), label="pop_1")
pop_1.record(["spikes", "v"])
sim.run(10)