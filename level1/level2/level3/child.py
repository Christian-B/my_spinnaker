import os
from level1.parent import Parent


class Child(Parent):

    def destory_path(self):
        p8_integration_tests_directory = os.path.dirname(__file__)
        test_dir = os.path.dirname(p8_integration_tests_directory)
        return os.path.join(test_dir, "JobDestroyedError.txt")

    def debug(self):
        print(self.destory_path())


if __name__ == '__main__':
    c = Child()
    c.debug()