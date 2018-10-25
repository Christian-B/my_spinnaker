import unittest


class LongTest(unittest.TestCase):

    def setUp(self):
        print("setup")

    def tearDown(self):
        print("teardown")

    # remove A to run but warning test never ends!
    def Atest_one(self):
        print("one")
        cutoff = 10000000
        i = 0
        while True:
            i += 1
            if i > cutoff:
                print(cutoff)
                cutoff += 1
                i = 0

    def test_two(self):
        print("two")
