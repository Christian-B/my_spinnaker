import time

its = 1000

start = time.time()


def a(xy):
    x, y = xy
    d = x + y  # noqa f841


def b(xy):
    d = xy[0] + xy[1]  # noqa f841


for i in range(its):
    for j in range(its):
        ij = (i, j)
        a(ij)

end = time.time()
print("x,y {}".format(end-start))

start = time.time()

for i in range(its):
    for j in range(its):
        ij = (i, j)
        b(ij)

end = time.time()

print("index {}".format(end-start))
