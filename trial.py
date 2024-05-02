import platform
import os

EXCLUDES = [".cache", ".git", ".idea", ".project", ".pytest_cache",
            ".pydevproject", ".settings",
            "application_generated_data_files", "reports"]


def _find_pyfiles(spynnaker8_dir, scripts_name, exceptions, broken):
    prefix_len = len(spynnaker8_dir) + 1
    script_dir = os.path.join(spynnaker8_dir, scripts_name)
    for root, dirs, files in os.walk(script_dir, topdown=True):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        files[:] = [f for f in files if f.endswith(".py")]
        root_extra = root[prefix_len:]
        if len(root_extra) > 0 and not os.path.exists(root_extra):
            os.mkdir(root_extra)
        if len(files) == 0:
            continue
        test_path = os.path.join(root_extra, "test_scripts.py")
        with open(test_path, "w") as test_file:
            test_file.write("# flake8: noqa\n")
            for script in files:
                if script in exceptions:
                    continue
                script_path = os.path.join(root, script)
                name = script_path[prefix_len:-3].replace(os.sep, "_")
                test_file.write("\n    def ")
                test_file.write(name)
                test_file.write("(self):\n        self.check_script(\"")
                the_path = os.path.abspath(script_path)
                # Paths are written to strings in files so Windows needs help!
                if platform.system() == "Windows":
                    the_path = the_path.replace("\\", "/")
                test_file.write(the_path)
                if script in broken:
                    test_file.write("\", True)\n\n    def test_")
                else:
                    test_file.write("\", False)\n\n    def test_")
                test_file.write(name)
                test_file.write("(self):\n        self.runsafe(self.")
                test_file.write(name)
                test_file.write(")\n")

if __name__ == '__main__':
    tests_dir = os.path.dirname(__file__)
    p8_integration_tests_dir = os.path.dirname(tests_dir)
    spynnaker8_dir = os.path.dirname(p8_integration_tests_dir)
    # Jenkins appears to place scripts one level higher
    if not os.path.exists(os.path.join(spynnaker8_dir, "IntroLab")):
        spynnaker8_dir = os.path.dirname(spynnaker8_dir)
    _find_pyfiles(spynnaker8_dir, "PyNNExamples",[],[])