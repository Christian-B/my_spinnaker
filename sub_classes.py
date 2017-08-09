import enum

print enum.version


class GrandParent(object):
    pass


class Parent1(GrandParent):
    @staticmethod
    def name():
        return "one"


class Parent2(GrandParent):
    @staticmethod
    def name():
        return "two"


class Child(Parent1, Parent2):
    pass


def subclasses_test(aclass):
    if not isinstance(aclass, type):
        aclass = type(aclass)
    print "subclasses_test"
    names = set()
    for sub in aclass.mro():
        print "sub", sub
        """
        if sub in GrandParent.__subclasses__():
            print sub.name()
        else:
            try:
                print sub.name()
            except:
                print "no name"
            print "skip"
        """
        if issubclass(sub, GrandParent) and not sub == GrandParent:
            names.add(sub.name())
    print list(names)
    print "==========="


# print(vars()['GrandParent'].__subclasses__())
grand_parent = GrandParent
# print grand_parent.__subclasses__()
# print GrandParent.__subclasses__()

# print Parent in grand_parent.__subclasses__()
# print Child in grand_parent.__subclasses__()

# print issubclass(Child, GrandParent)

# print type(module).mro()
# print Child.mro()

child = Child()
subclasses_test(child)
