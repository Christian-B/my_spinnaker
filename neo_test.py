import numpy as np
from quantities import Hz
from neo import AnalogSignal as AnalogSignal

n = np.array([[0.1, 0.1, 0.1, 0.1],
              [-2.0, -2.0, -2.0, -4.0],
              [0.1, 0.1, 0.1, 0.1],
              [-0.1, -0.1, -0.1, -0.1],
              [-0.1, -0.1, -0.1, -0.1],
              [-3.0, -3.0, -3.0, -3.0],
              [0.1, 0.1, 0.1, 0.1],
              [0.1, 0.1, 0.1, 0.1]])

a = AnalogSignal(n, sampling_rate=1000*Hz, units='V')

print n
print n[1, 3]
print n.shape
print n[:, 0]

print a
print a[1, 3]
print a.magnitude.shape
print a.magnitude[:, 0]
