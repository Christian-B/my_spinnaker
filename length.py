class IterOnly(object):

    def __iter__(self):
        for x in range(5):
            yield x


test = IterOnly()
for x in test:
    print x

print test[3]
print len(test)
