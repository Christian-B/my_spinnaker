import time


def foo(a, b):
    c = a - b
    print c


t0 = time.time()
for i in xrange(10000):
    foo(6, 10)
t1 = time.time()

print t1-t0
