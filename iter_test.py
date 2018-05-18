import math
import time


def is_prime(number):
    for current in range(3, int(math.sqrt(number) + 1), 2):
        if number % current == 0:
            return False
    return True


def get_primes():
    yield 2
    yield 3
    number = 5
    while True:
        if is_prime(number):
            yield number
        number += 2


def do_check(candidate, primes, end):
    for i in range(end):
        if candidate % primes[i] == 0:
            return False
    # for check in primes[:end]:
    #    if candidate % check == 0:
    #        return False
    return True


def get_primes2():
    primes = [2, 3, 5, 7]
    for p in primes:
        yield p
    candidate = 11
    end = 2
    while True:
        if primes[end] * primes[end] <= candidate:
            end += 1
        if do_check(candidate, primes, end):
            primes.append(candidate)
            yield candidate
        candidate += 2


def solve_number_10():
    # She *is* working on Project Euler #10, I knew it!
    total = 2
    for next_prime in get_primes():
        if next_prime < 2000000:
            total += next_prime
        else:
            print(total)
            return

# for value in get_primes2():
#    print(value)
#    if value > 200:
#        exit(1)


start = time.time()
solve_number_10()
end = time.time()
print(end - start)


"""
2000000
142913828924
a) 32.315999984
b) 28.6239998341
c) 29.0099999905
d) 28.7089998722


200000
1709600815
a) 1.61599993706
b) 1.41899991035
c) 1.34999990463

200
4229
a) 0.000999927520752
b) 0.000999927520752
"""
