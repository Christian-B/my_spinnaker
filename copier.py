import os
import shutil

path = "/brenninc/spinnaker/sPyNNaker/integration_testsX"
for root, dirs, files in os.walk(path, topdown=True):
    for name in files:
        if name.endswith(".py"):
            path = os.path.join(root, name)
            print path
            target = path.replace("integration_testsX", "integration_tests")
            print target
            if os.path.exists(target):
                os.remove(target)
            shutil.copyfile(path, target)
