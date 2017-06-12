import inspect


def called():
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    print 'caller file:', calframe[1][1]
    print 'caller line:', calframe[1][2]
    print 'caller name:', calframe[1][3]
