all_dict = set()

def check(path):
    print(path)
    with open(path) as a_dict:
        for line in a_dict:
            line = line.strip()
            if len(line) > 1 and not line.startswith("#"):
                if line in all_dict:
                    print(line)
                else:
                    all_dict.add(line)

check("/home/brenninc/spinnaker/SupportScripts/actions/pylint/default_dict.txt")
check("/home/brenninc/spinnaker/SpiNNUtils/.pylint_dict.txt")
check("/home/brenninc/spinnaker/SpiNNMachine/.pylint_dict.txt")
check("/home/brenninc/spinnaker/SpiNNMan/.pylint_dict.txt")
check("/home/brenninc/spinnaker/PACMAN/.pylint_dict.txt")
check("/home/brenninc/spinnaker/SpiNNFrontEndCommon/.pylint_dict.txt")
check("/home/brenninc/spinnaker/TestBase/.pylint_dict.txt")
check("/home/brenninc/spinnaker/sPyNNaker/.pylint_dict.txt")
check("/home/brenninc/spinnaker/SpiNNakerGraphFrontEnd/.pylint_dict.txt")
print(all_dict)
