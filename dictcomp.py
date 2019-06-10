import time
import numpy

tuplelist = []
for i in range(100):
    for j in range(100):
        tuplelist.append((i, j))

start = time.time()
direct = dict()
for i in range(100):
    for j in range(100):
        direct[(i, j)] = str(i) + str(j)
end = time.time()
print("direct", end - start)

start = time.time()
indirect = dict()
for i in range(100):
    inner = dict()
    for j in range(100):
        inner[j] = str(i) + str(j)
    indirect[i] = inner
end = time.time()
print("indirect", end - start)

start = time.time()
indirect2 = [None] * 100
for i in range(100):
    inner = [None] * 100
    for j in range(100):
        inner[j] = str(i) + str(j)
    indirect2[i] = inner
end = time.time()
print("lists", end - start)

start = time.time()
indirect3 = numpy.empty([100, 100], dtype=str)
for i in range(100):
    for j in range(100):
        indirect3[i, j] = str(i) + str(j)
end = time.time()
print("numpy", end - start)

start = time.time()
for x in range(1000):
    for i in range(100):
        for j in range(100):
            a = direct[(i, j)]
end = time.time()
print("direct", end - start)

start = time.time()
for x in range(1000):
    for tuple in tuplelist:
        a = direct[tuple]
end = time.time()
print("tuple", end - start)

start = time.time()
for x in range(1000):
    for i in range(100):
        for j in range(100):
            a = indirect[i][j]
end = time.time()
print("indirect", end - start)

start = time.time()
for x in range(1000):
    for i in range(100):
        for j in range(100):
            a = indirect.get(i).get(j)
end = time.time()
print("indirect get", end - start)

start = time.time()
for x in range(1000):
    for i in range(100):
        for j in range(100):
            a = indirect2[i][j]
end = time.time()
print("lists", end - start)

start = time.time()
for x in range(1000):
    for i in range(100):
        for j in range(100):
            a = indirect3[i, j]
end = time.time()
print("numpy", end - start)
