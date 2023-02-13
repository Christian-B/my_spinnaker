import time
def foo():
    return 1

def level4():
    a = foo()

def level3():
    level4()

def level2():
    level3()

def level1():
    level2()

def leveld(v):
    a = v

def levelc(v):
    leveld(v)

def levelb(v):
    levelc(v)

def levela(v):
    levelb(v)

n = 10000000
start = time.time()
for i in range(n):
    level1()
print(time.time() - start)
start = time.time()
for i in range(n):
    levela(1)
print(time.time() - start)