import pickle

with open("spikes.pickle", "r") as spike_file:
    block = pickle.load(spike_file)

segment = block.segments[0]
spiketrain = segment.spiketrains
print type(spiketrain)

print len(spiketrain)

lengths = map(len, spiketrain)
print lengths

total = reduce(lambda x, y: x + y, lengths)
print total

num_spikes = reduce(lambda x, y: x + y,
                    map(len, block.segments[0].spiketrains))
print num_spikes
