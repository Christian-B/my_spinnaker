import unittest
# import pytest.mark


def fun(x):
    return x + 1


class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 5)

    def test_hang(self):
        x = 0
        y = 1000000
        while True:
            x = fun(x)
            if x >= y:
                print x
                x = 0
                y += 1

    def test_hang2(self):
        x = 0
        y = 1000000
        while True:
            x = fun(x)
            if x >= y:
                print x
                x = 0
                y += 1
