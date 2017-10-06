from neo.core import (Block, Segment, ChannelIndex, AnalogSignal)
from quantities import nA, kHz, ms
import numpy as np
import neo
import pickle

blk = Block()
seg = Segment(name='segment foo')
blk.segments.append(seg)

source_ids = np.arange(64)
channel_ids = source_ids + 42
chx = ChannelIndex(name='Array probe', index=np.arange(64), channel_ids=channel_ids,
                   channel_names=['Channel %i' % chid for chid in channel_ids])
blk.channel_indexes.append(chx)

a = AnalogSignal(np.random.randn(10000, 64)*nA, sampling_rate=10*kHz)

# link AnalogSignal and ID providing channel_index
a.channel_index = chx
chx.analogsignals.append(a)
seg.analogsignals.append(a)

seg1 = blk.segments[0]
a1 = seg1.analogsignals[0]
chx1 = a1.channel_index
print chx1
print chx1.index

io = neo.io.PickleIO(filename="test.pickle")
io.write(blk)

with open("test.pickle", "r") as pickle_file:
    blk2 = pickle.load(pickle_file)

seg2 = blk2.segments[0]
a2 = seg2.analogsignals[0]
chx2 = a2.channel_index
print chx2
print chx2.index

