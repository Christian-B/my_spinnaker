from collections import namedtuple
import time
from typing import NamedTuple


class Foo(object):

    __slots__ = ("alpha", "beta", "gamma")

    def __init__(self, alpha, beta, gamma):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

Bar = namedtuple('Bar', ['alpha', 'beta', 'gamma'])


class Gamma(object):

    __slots__ = ("_alpha", "_beta", "_gamma")

    def __init__(self, alpha, beta, gamma):
        self._alpha = alpha
        self._beta = beta
        self._gamma = gamma

    @property
    def alpha(self):
        return self._alpha

    @property
    def beta(self):
        return self._beta

    @property
    def gamma(self):
        return self._gamma

class Epsilon(NamedTuple):
    alpha:int
    beta:int
    gamma:int

class Bacon(object):

    def __init__(self, alpha, beta, gamma):
        self._alpha = alpha
        self._beta = beta
        self._gamma = gamma

    @property
    def alpha(self):
        return self._alpha

    @property
    def beta(self):
        return self._beta

    @property
    def gamma(self):
        return self._gamma

class Eggs(object):

    def __init__(self, alpha, beta, gamma):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma


loops = 1000000

start = time.time()
for i in range(loops):
    foo = Foo(1,2,3)
    a = foo.alpha
    b = foo.beta
    c = foo.gamma
end = time.time()
print("Foo", end-start)

start = time.time()
for i in range(loops):
    bar = Bar(1,2,3)
    a = bar.alpha
    b = bar.beta
    c= foo.gamma
end = time.time()
print("Bar", end-start)

start = time.time()
for i in range(loops):
    gamma = Gamma(1,2,3)
    a = gamma.alpha
    g = gamma.beta
    c = gamma.gamma
end = time.time()
print("Gamma", end-start)

start = time.time()
for i in range(loops):
    epsilon = Epsilon(1,2,3)
    a = epsilon.alpha
    b = epsilon.beta
    c = epsilon.gamma
end = time.time()
print("Epsilon", end-start)
boo = Epsilon("a","2","3")
print(boo)

start = time.time()
for i in range(loops):
    bacon = Bacon(1,2,3)
    a = bacon.alpha
    b = bacon.beta
    c = bacon.gamma
end = time.time()
print("Bacon", end-start)

start = time.time()
for i in range(loops):
    eggs = Eggs(1,2,3)
    a = eggs.alpha
    b = eggs.beta
    c = eggs.gamma
end = time.time()
print("Eggs", end-start)
